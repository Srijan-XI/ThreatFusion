import React, { useState, useEffect } from 'react';
import { 
  Shield, 
  Terminal, 
  Activity, 
  Cpu, 
  Zap, 
  FolderTree, 
  ChevronRight, 
  Code, 
  Server, 
  Lock,
  Menu,
  X
} from 'lucide-react';

const ThreatFusionLanding = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [activeTab, setActiveTab] = useState('overview');
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollToSection = (id) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
    setIsMenuOpen(false);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 font-sans selection:bg-emerald-500/30 selection:text-emerald-200">
      {/* Navigation */}
      <nav className={`fixed w-full z-50 transition-all duration-300 border-b ${scrolled ? 'bg-slate-950/90 backdrop-blur-md border-emerald-900/30 py-4' : 'bg-transparent border-transparent py-6'}`}>
        <div className="container mx-auto px-6 flex justify-between items-center">
          <div className="flex items-center gap-2 group cursor-pointer" onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}>
            <div className="relative">
              <Shield className="w-8 h-8 text-emerald-500 group-hover:animate-pulse" />
              <div className="absolute inset-0 bg-emerald-500/20 blur-lg rounded-full animate-pulse"></div>
            </div>
            <span className="text-xl font-bold tracking-tighter text-white">
              Threat<span className="text-emerald-500">Fusion</span>
            </span>
          </div>

          {/* Desktop Nav */}
          <div className="hidden md:flex items-center gap-8">
            {['Overview', 'Structure', 'Usage', 'Roadmap'].map((item) => (
              <button 
                key={item}
                onClick={() => scrollToSection(item.toLowerCase())}
                className="text-sm font-medium text-slate-400 hover:text-emerald-400 transition-colors uppercase tracking-widest"
              >
                {item}
              </button>
            ))}
            <a 
              href="#"
              className="px-5 py-2 bg-emerald-600/10 border border-emerald-500/50 text-emerald-400 rounded hover:bg-emerald-500 hover:text-slate-950 transition-all duration-300 font-medium text-sm"
            >
              Get Started
            </a>
          </div>

          {/* Mobile Menu Button */}
          <button 
            className="md:hidden text-slate-300 hover:text-emerald-400"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            {isMenuOpen ? <X /> : <Menu />}
          </button>
        </div>

        {/* Mobile Nav */}
        {isMenuOpen && (
          <div className="md:hidden absolute top-full left-0 w-full bg-slate-900 border-b border-emerald-900/30 py-4 px-6 flex flex-col gap-4">
            {['Overview', 'Structure', 'Usage', 'Roadmap'].map((item) => (
              <button 
                key={item}
                onClick={() => scrollToSection(item.toLowerCase())}
                className="text-left text-slate-300 hover:text-emerald-400 py-2"
              >
                {item}
              </button>
            ))}
          </div>
        )}
      </nav>

      {/* Hero Section */}
      <section className="relative pt-32 pb-20 overflow-hidden">
        {/* Background Grid */}
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#0f172a_1px,transparent_1px),linear-gradient(to_bottom,#0f172a_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)] opacity-20 pointer-events-none"></div>
        
        <div className="container mx-auto px-6 relative z-10">
          <div className="flex flex-col lg:flex-row items-center gap-12">
            <div className="lg:w-1/2 space-y-8">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-950/50 border border-emerald-800/50 text-emerald-400 text-xs font-mono">
                <span className="relative flex h-2 w-2">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                </span>
                v1.0.0 Stable Release
              </div>
              
              <h1 className="text-5xl lg:text-7xl font-bold leading-tight">
                Unified <br />
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-cyan-500">
                  Cybersecurity
                </span> <br />
                Analysis Platform
              </h1>
              
              <p className="text-lg text-slate-400 max-w-xl leading-relaxed">
                ThreatFusion is a modular threat detection engine utilizing C++, Python, and Go. 
                Leverage network scanning, heuristic log analysis, and behavioral detection for a 
                comprehensive security posture.
              </p>
              
              <div className="flex flex-wrap gap-4">
                <button 
                  onClick={() => scrollToSection('usage')}
                  className="px-8 py-4 bg-emerald-500 text-slate-950 font-bold rounded hover:bg-emerald-400 transition-colors flex items-center gap-2"
                >
                  <Terminal className="w-5 h-5" />
                  Start Analyzing
                </button>
                <button 
                  onClick={() => scrollToSection('structure')}
                  className="px-8 py-4 bg-slate-900 border border-slate-700 text-slate-300 font-bold rounded hover:border-emerald-500/50 hover:text-emerald-400 transition-all flex items-center gap-2"
                >
                  <FolderTree className="w-5 h-5" />
                  View Architecture
                </button>
              </div>
            </div>
            
            <div className="lg:w-1/2 w-full">
              <div className="relative rounded-xl border border-emerald-900/50 bg-slate-950/80 shadow-2xl overflow-hidden backdrop-blur-sm group">
                <div className="absolute inset-0 bg-gradient-to-br from-emerald-500/5 to-purple-500/5 group-hover:opacity-100 transition-opacity opacity-50"></div>
                
                {/* Window Controls */}
                <div className="flex items-center gap-2 px-4 py-3 border-b border-slate-800 bg-slate-900/50">
                  <div className="w-3 h-3 rounded-full bg-rose-500/50"></div>
                  <div className="w-3 h-3 rounded-full bg-amber-500/50"></div>
                  <div className="w-3 h-3 rounded-full bg-emerald-500/50"></div>
                  <div className="ml-auto text-xs text-slate-500 font-mono">user@threatfusion:~</div>
                </div>
                
                {/* Terminal Content */}
                <div className="p-6 font-mono text-sm space-y-4">
                  <div className="flex gap-2">
                    <span className="text-emerald-500">➜</span>
                    <span className="text-cyan-400">~/ThreatFusion</span>
                    <span className="text-slate-400">$ python -m analyzer_py.analyzer</span>
                  </div>
                  <div className="space-y-1 text-slate-300">
                    <div className="text-emerald-400">[INFO] Initializing ThreatFusion Core...</div>
                    <div>[+] Loading Heuristic Models... <span className="text-emerald-500">DONE</span></div>
                    <div>[+] Network Scanner (C++) attached.</div>
                    <div>[+] NetAnalyzer (Go) service ready.</div>
                    <div className="animate-pulse text-amber-400">[!] Analyzing logs/access.log...</div>
                    <div className="pl-4 text-slate-500 border-l border-slate-700">
                      Found 3 suspicious entries.<br/>
                      IP: 192.168.1.45 - SQL Injection Attempt<br/>
                      Confidence: 98%
                    </div>
                  </div>
                  <div className="flex gap-2 pt-2">
                    <span className="text-emerald-500">➜</span>
                    <span className="text-cyan-400">~/ThreatFusion</span>
                    <span className="w-2 h-5 bg-slate-500 animate-pulse"></span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Tech Stack / Overview Section */}
      <section id="overview" className="py-20 bg-slate-900/50 border-y border-slate-800">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold mb-4">Core Technology Stack</h2>
            <p className="text-slate-400">Built for speed, interoperability, and scalability.</p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <FeatureCard 
              icon={<Code className="w-8 h-8 text-blue-400" />}
              title="Python Analyzer"
              desc="The brain of the operation. Handles log analysis, heuristics management, and high-level orchestration using Pandas and Scikit-learn."
              tags={['Pandas', 'Scikit-learn', 'Matplotlib']}
            />
            <FeatureCard 
              icon={<Cpu className="w-8 h-8 text-rose-400" />}
              title="C++ Scanner"
              desc="High-performance network scanner for rapid port discovery and service identification. Utilizing C++17 for optimal speed."
              tags={['C++17', 'Low-level Networking', 'Speed']}
            />
            <FeatureCard 
              icon={<Zap className="w-8 h-8 text-cyan-400" />}
              title="Go NetAnalyzer"
              desc="Concurrency-focused tool for handling real-time network analysis tasks and scalable data ingestion."
              tags={['Golang', 'Concurrency', 'Scalable']}
            />
          </div>
        </div>
      </section>

      {/* Project Structure */}
      <section id="structure" className="py-20 bg-slate-950">
        <div className="container mx-auto px-6">
          <div className="flex flex-col md:flex-row gap-12 items-start">
            <div className="md:w-1/3">
              <h2 className="text-3xl font-bold mb-6 flex items-center gap-3">
                <FolderTree className="text-emerald-500" />
                Project Structure
              </h2>
              <p className="text-slate-400 mb-6">
                A modular architecture separating concerns between high-level analysis and low-level scanning capabilities.
              </p>
              <div className="p-4 bg-slate-900 rounded-lg border border-slate-800">
                <h3 className="text-sm font-semibold text-slate-300 mb-2 uppercase tracking-wider">Prerequisites</h3>
                <ul className="space-y-3 text-sm text-slate-400">
                  <li className="flex items-center gap-2">
                    <ChevronRight className="w-4 h-4 text-emerald-500" />
                    C++17 Compiler (g++)
                  </li>
                  <li className="flex items-center gap-2">
                    <ChevronRight className="w-4 h-4 text-emerald-500" />
                    Python 3.8+ (Tested 3.13.7)
                  </li>
                  <li className="flex items-center gap-2">
                    <ChevronRight className="w-4 h-4 text-emerald-500" />
                    Go Environment
                  </li>
                  <li className="flex items-center gap-2">
                    <ChevronRight className="w-4 h-4 text-emerald-500" />
                    Pandas, Matplotlib, Scikit-learn
                  </li>
                </ul>
              </div>
            </div>

            <div className="md:w-2/3 bg-slate-900 rounded-xl p-8 border border-slate-800 font-mono text-sm shadow-xl">
              <div className="text-slate-300 space-y-2">
                <div className="flex items-center gap-2 text-emerald-400 font-bold">
                  <FolderTree className="w-4 h-4" /> ThreatFusion/
                </div>
                
                <div className="pl-6 space-y-2 border-l border-slate-800 ml-2">
                  <TreeItem name="analyzer_py/" comment="# Python module for logic & heuristics" isFolder>
                    <TreeItem name="init.py" />
                    <TreeItem name="analyzer.py" />
                    <TreeItem name="models/" isFolder>
                      <TreeItem name="init.py" />
                      <TreeItem name="heuristics.py" />
                    </TreeItem>
                  </TreeItem>

                  <TreeItem name="scanner_cpp/" comment="# High-perf network scanner" isFolder>
                    <TreeItem name="main.cpp" />
                    <TreeItem name="scanner.hpp" />
                    <TreeItem name="utils.cpp" />
                  </TreeItem>

                  <TreeItem name="net_analyzer_go/" comment="# Concurrent network tools" isFolder>
                    <TreeItem name="netscan.go" />
                  </TreeItem>

                  <TreeItem name="outputs/" isFolder>
                    <TreeItem name="logs/" comment="# Input directory for logs" isFolder />
                  </TreeItem>
                  
                  <TreeItem name="README.md" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Setup & Usage */}
      <section id="usage" className="py-20 relative overflow-hidden">
        {/* Decorative elements */}
        <div className="absolute top-0 right-0 w-1/3 h-full bg-gradient-to-l from-emerald-900/10 to-transparent pointer-events-none"></div>

        <div className="container mx-auto px-6 relative">
          <h2 className="text-3xl font-bold mb-12 text-center">Setup & Usage Protocols</h2>

          <div className="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto">
            
            {/* Python Guide */}
            <div className="bg-slate-900/80 p-6 rounded-xl border border-emerald-900/30 hover:border-emerald-500/50 transition-colors group">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-xl font-semibold text-emerald-400">Python Log Analyzer</h3>
                <Terminal className="text-slate-600 group-hover:text-emerald-500 transition-colors" />
              </div>
              <ol className="list-decimal list-inside space-y-4 text-slate-400 mb-6">
                <li>Place your <code className="bg-slate-800 px-1 py-0.5 rounded text-slate-200">.log</code> files inside <code className="bg-slate-800 px-1 py-0.5 rounded text-emerald-300">outputs/logs/</code></li>
                <li>Execute the analyzer module:</li>
              </ol>
              <div className="bg-black p-4 rounded border border-slate-800 font-mono text-sm text-slate-300 group-hover:border-emerald-500/30 transition-colors">
                $ python -m analyzer_py.analyzer
              </div>
            </div>

            {/* C++ & Go Guide */}
            <div className="bg-slate-900/80 p-6 rounded-xl border border-slate-800 hover:border-blue-500/50 transition-colors group">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-xl font-semibold text-blue-400">Scanner Modules</h3>
                <Activity className="text-slate-600 group-hover:text-blue-500 transition-colors" />
              </div>
              
              <div className="space-y-6">
                <div>
                  <h4 className="text-sm font-bold text-slate-300 uppercase mb-2">C++ Scanner</h4>
                  <p className="text-sm text-slate-400 mb-2">Compile and run directly in the directory.</p>
                  <div className="bg-black p-3 rounded border border-slate-800 font-mono text-xs text-slate-400">
                    cd scanner_cpp/ && g++ main.cpp -o scanner
                  </div>
                </div>

                <div>
                  <h4 className="text-sm font-bold text-slate-300 uppercase mb-2">Go Network Analyzer</h4>
                  <p className="text-sm text-slate-400 mb-2">Build the utility for concurrent scanning.</p>
                  <div className="bg-black p-3 rounded border border-slate-800 font-mono text-xs text-slate-400">
                    go build netscan.go
                  </div>
                </div>
              </div>
            </div>

          </div>
        </div>
      </section>

      {/* Roadmap */}
      <section id="roadmap" className="py-20 bg-slate-900/50">
        <div className="container mx-auto px-6">
          <h2 className="text-3xl font-bold mb-12 text-center">Project Vision</h2>
          
          <div className="grid md:grid-cols-4 gap-6">
            <RoadmapItem 
              icon={<Cpu />} 
              title="ML Integration" 
              desc="Expand heuristic detection rules with advanced machine learning techniques." 
            />
            <RoadmapItem 
              icon={<Activity />} 
              title="Automation" 
              desc="Full pipeline automation for continuous monitoring and real-time alerting." 
            />
            <RoadmapItem 
              icon={<Lock />} 
              title="Secure Comms" 
              desc="Encrypted IPC between C++, Go, and Python modules." 
            />
            <RoadmapItem 
              icon={<Server />} 
              title="Documentation" 
              desc="Extensive usage cases and threat scenarios for operational readiness." 
            />
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 border-t border-slate-800 bg-slate-950">
        <div className="container mx-auto px-6 text-center">
          <div className="flex items-center justify-center gap-2 mb-6">
            <Shield className="w-6 h-6 text-emerald-600" />
            <span className="text-lg font-bold tracking-tighter text-slate-500">
              Threat<span className="text-emerald-700">Fusion</span>
            </span>
          </div>
          <p className="text-slate-500 max-w-2xl mx-auto mb-8">
            This project honors the discipline and legacy of cybersecurity professionals. 
            Contributions that uphold these standards are welcome.
          </p>
          <div className="flex justify-center gap-6 text-sm text-slate-600">
            <a href="#" className="hover:text-emerald-500 transition-colors">GitHub</a>
            <a href="#" className="hover:text-emerald-500 transition-colors">Documentation</a>
            <a href="#" className="hover:text-emerald-500 transition-colors">License</a>
          </div>
          <p className="mt-8 text-xs text-slate-700">
            © 2025 ThreatFusion Project. All systems nominal.
          </p>
        </div>
      </footer>
    </div>
  );
};

const FeatureCard = ({ icon, title, desc, tags }) => (
  <div className="bg-slate-950 p-6 rounded-xl border border-slate-800 hover:border-emerald-500/30 hover:shadow-lg hover:shadow-emerald-500/10 transition-all duration-300">
    <div className="mb-4 bg-slate-900 w-14 h-14 rounded-lg flex items-center justify-center border border-slate-800">
      {icon}
    </div>
    <h3 className="text-xl font-bold mb-3 text-slate-200">{title}</h3>
    <p className="text-slate-400 text-sm leading-relaxed mb-6 h-20">
      {desc}
    </p>
    <div className="flex flex-wrap gap-2">
      {tags.map((tag) => (
        <span key={tag} className="text-xs px-2 py-1 bg-slate-900 text-slate-400 rounded border border-slate-800">
          {tag}
        </span>
      ))}
    </div>
  </div>
);

const TreeItem = ({ name, comment, isFolder, children }) => (
  <div className="relative">
    <div className="flex items-center gap-2 py-1 hover:bg-slate-800/50 rounded px-2 transition-colors -ml-2">
      {isFolder ? <FolderTree className="w-4 h-4 text-emerald-600" /> : <ChevronRight className="w-3 h-3 text-slate-600" />}
      <span className={isFolder ? "text-emerald-200" : "text-slate-300"}>{name}</span>
      {comment && <span className="text-slate-600 text-xs italic hidden sm:inline ml-2">{comment}</span>}
    </div>
    {children && (
      <div className="pl-6 border-l border-slate-800 ml-2.5 my-1">
        {children}
      </div>
    )}
  </div>
);

const RoadmapItem = ({ icon, title, desc }) => (
  <div className="bg-slate-950 p-6 rounded-xl border border-slate-800 text-center hover:border-emerald-500/30 transition-colors">
    <div className="mx-auto mb-4 bg-slate-900 w-12 h-12 rounded-full flex items-center justify-center text-emerald-500 border border-slate-800">
      {icon}
    </div>
    <h3 className="font-bold text-lg mb-2">{title}</h3>
    <p className="text-sm text-slate-400">{desc}</p>
  </div>
);

export default ThreatFusionLanding;