package main

import (
	"encoding/json"
	"fmt"
	"net"
	"os"
	"path/filepath"
	"sort"
	"strconv"
	"strings"
	"sync"
	"time"
)

var (
	logFile = "outputs/logs/netscan.log"
	// Default service set balances speed with practical exposure coverage.
	defaultPorts = []int{21, 22, 23, 80, 443, 445, 3306, 3389, 8080}
	wg           sync.WaitGroup
)

type HostResult struct {
	IP        string `json:"ip"`
	Hostname  string `json:"hostname,omitempty"`
	OpenPorts []int  `json:"open_ports"`
	// RiskLevel is derived from exposed port profile, not traffic behavior.
	RiskLevel string `json:"risk_level"`
}

type ScanSummary struct {
	Timestamp          string       `json:"timestamp"`
	Subnet             string       `json:"subnet"`
	ScannedHosts       int          `json:"scanned_hosts"`
	HostsWithOpenPorts int          `json:"hosts_with_open_ports"`
	TotalOpenPorts     int          `json:"total_open_ports"`
	DurationMs         int64        `json:"duration_ms"`
	Results            []HostResult `json:"results"`
}

func main() {
	start := time.Now()
	// Configuration can be overridden by environment variables.
	subnet := getSubnetPrefix()
	ports := getPorts()
	// Buffered channel prevents result producers from blocking excessively.
	resultsCh := make(chan HostResult, 254)

	fmt.Println("[*] Starting network scan on subnet:", subnet)
	fmt.Println("[*] Active scan ports:", ports)

	// Ensure output directories exist.
	logDir := filepath.Dir(logFile)
	if err := os.MkdirAll(logDir, 0755); err != nil {
		fmt.Println("[-] Unable to create log directory.")
		return
	}
	if err := os.MkdirAll("outputs/network", 0755); err != nil {
		fmt.Println("[-] Unable to create network output directory.")
		return
	}

	file, err := os.Create(logFile)
	if err != nil {
		fmt.Println("[-] Unable to create log file.")
		return
	}
	defer file.Close()
	_, _ = file.WriteString(fmt.Sprintf("ThreatFusion Go NetScan\nSubnet: %s\nPorts: %v\nStarted: %s\n\n", subnet, ports, time.Now().Format(time.RFC3339)))

	for i := 1; i <= 254; i++ {
		ip := subnet + strconv.Itoa(i)
		wg.Add(1)
		// One goroutine per host for fast subnet fan-out scanning.
		go scanIP(ip, ports, resultsCh)
	}
	wg.Wait()
	close(resultsCh)

	results := make([]HostResult, 0)
	totalOpenPorts := 0
	// Collect only hosts with findings to keep reports compact and relevant.
	for res := range resultsCh {
		if len(res.OpenPorts) > 0 {
			results = append(results, res)
			totalOpenPorts += len(res.OpenPorts)
		}
	}

	sort.Slice(results, func(i, j int) bool {
		return results[i].IP < results[j].IP
	})

	for _, res := range results {
		line := fmt.Sprintf("[!] Host: %s | Ports: %v | Risk: %s", res.IP, res.OpenPorts, res.RiskLevel)
		if res.Hostname != "" {
			line += fmt.Sprintf(" | Hostname: %s", res.Hostname)
		}
		line += "\n"
		fmt.Print(line)
		_, _ = file.WriteString(line)
	}

	summary := ScanSummary{
		Timestamp:          time.Now().Format(time.RFC3339),
		Subnet:             subnet,
		ScannedHosts:       254,
		HostsWithOpenPorts: len(results),
		TotalOpenPorts:     totalOpenPorts,
		DurationMs:         time.Since(start).Milliseconds(),
		Results:            results,
	}

	_ = writeJSONReport(summary)
	_, _ = file.WriteString(fmt.Sprintf("\nCompleted: %s\nHosts with open ports: %d\nTotal open ports: %d\nDuration(ms): %d\n", time.Now().Format(time.RFC3339), summary.HostsWithOpenPorts, summary.TotalOpenPorts, summary.DurationMs))
	fmt.Println("[+] Network scan completed. Results saved to:", logFile)
}

func scanIP(ip string, ports []int, resultsCh chan<- HostResult) {
	defer wg.Done()

	open := make([]int, 0)
	// TCP connect scan: successful connection implies open/listening port.
	for _, port := range ports {
		address := fmt.Sprintf("%s:%d", ip, port)
		conn, err := net.DialTimeout("tcp", address, 300*time.Millisecond)
		if err == nil {
			open = append(open, port)
			_ = conn.Close()
		}
	}

	if len(open) == 0 {
		return
	}

	// Reverse DNS is best-effort and time-bounded to avoid slowing scans.
	hostname := reverseLookupWithTimeout(ip, 350*time.Millisecond)
	resultsCh <- HostResult{
		IP:        ip,
		Hostname:  hostname,
		OpenPorts: open,
		RiskLevel: assessRisk(open),
	}
}

func getSubnetPrefix() string {
	// Expected format: "192.168.1." (trailing dot auto-fixed if omitted).
	subnet := strings.TrimSpace(os.Getenv("THREATFUSION_SUBNET"))
	if subnet == "" {
		return "192.168.1."
	}
	if !strings.HasSuffix(subnet, ".") {
		subnet += "."
	}
	return subnet
}

func getPorts() []int {
	// Expected format: comma-separated integers, e.g., "22,80,443".
	raw := strings.TrimSpace(os.Getenv("THREATFUSION_PORTS"))
	if raw == "" {
		return defaultPorts
	}

	ports := make([]int, 0)
	seen := make(map[int]bool)
	for _, token := range strings.Split(raw, ",") {
		value := strings.TrimSpace(token)
		if value == "" {
			continue
		}
		p, err := strconv.Atoi(value)
		// Ignore malformed/out-of-range entries to keep parsing fault-tolerant.
		if err != nil || p < 1 || p > 65535 {
			continue
		}
		if !seen[p] {
			seen[p] = true
			ports = append(ports, p)
		}
	}
	if len(ports) == 0 {
		// Fall back to defaults if all provided values were invalid.
		return defaultPorts
	}
	// Sort for deterministic output and easier report comparisons.
	sort.Ints(ports)
	return ports
}

func reverseLookupWithTimeout(ip string, timeout time.Duration) string {
	type lookupResult struct {
		hostname string
	}
	ch := make(chan lookupResult, 1)

	go func() {
		names, err := net.LookupAddr(ip)
		if err != nil || len(names) == 0 {
			ch <- lookupResult{hostname: ""}
			return
		}
		host := strings.TrimSuffix(names[0], ".")
		ch <- lookupResult{hostname: host}
	}()

	select {
	case r := <-ch:
		return r.hostname
	case <-time.After(timeout):
		// DNS latency should not block the scan pipeline.
		return ""
	}
}

func assessRisk(openPorts []int) string {
	if len(openPorts) == 0 {
		return "LOW"
	}

	// Heuristic score: higher weights for frequently abused or sensitive ports.
	score := 0
	for _, p := range openPorts {
		switch p {
		case 21, 23, 445, 3306, 3389:
			score += 3
		case 22, 80, 8080:
			score += 2
		case 443:
			score += 1
		default:
			score += 1
		}
	}

	switch {
	// Threshold bands map numeric score to human-readable severity.
	case score >= 8:
		return "CRITICAL"
	case score >= 5:
		return "HIGH"
	case score >= 3:
		return "MEDIUM"
	default:
		return "LOW"
	}
}

func writeJSONReport(summary ScanSummary) error {
	// Timestamped filenames keep historical snapshots without overwrite.
	outputFile := filepath.Join("outputs", "network", fmt.Sprintf("network_analysis_%s.json", time.Now().Format("20060102_150405")))
	body, err := json.MarshalIndent(summary, "", "  ")
	if err != nil {
		fmt.Println("[-] Unable to serialize JSON report:", err)
		return err
	}
	if err := os.WriteFile(outputFile, body, 0644); err != nil {
		fmt.Println("[-] Unable to write JSON report:", err)
		return err
	}
	fmt.Println("[+] JSON report generated:", outputFile)
	return nil
}
