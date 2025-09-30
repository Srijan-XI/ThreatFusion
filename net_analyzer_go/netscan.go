package main

import (
	"fmt"
	"net"
	"os"
	"path/filepath"
	"strconv"
	"sync"
	"time"
)

var (
	logFile   = "outputs/logs/netscan.log"
	openPorts = []int{21, 22, 23, 80, 443, 3306, 8080}
	wg        sync.WaitGroup
	fileMutex sync.Mutex // Add a mutex for file writes
)

func main() {
	subnet := "192.168.1." // Sample subnet
	fmt.Println("[*] Starting network scan on subnet:", subnet)

	// Ensure log directory exists
	logDir := filepath.Dir(logFile)
	if err := os.MkdirAll(logDir, 0755); err != nil {
		fmt.Println("[-] Unable to create log directory.")
		return
	}

	file, err := os.Create(logFile)
	if err != nil {
		fmt.Println("[-] Unable to create log file.")
		return
	}
	defer file.Close()

	for i := 1; i <= 254; i++ {
		ip := subnet + strconv.Itoa(i)
		wg.Add(1)
		go scanIP(ip, file)
	}
	wg.Wait()
	fmt.Println("[+] Network scan completed. Results saved to:", logFile)
}

func scanIP(ip string, file *os.File) {
	defer wg.Done()

	for _, port := range openPorts {
		address := fmt.Sprintf("%s:%d", ip, port)
		conn, err := net.DialTimeout("tcp", address, 300*time.Millisecond)
		if err == nil {
			log := fmt.Sprintf("[!] Open Port Detected: %s\n", address)
			fmt.Print(log)
			fileMutex.Lock() // Lock before writing
			file.WriteString(log)
			fileMutex.Unlock() // Unlock after writing
			conn.Close()
		}
	}
}
