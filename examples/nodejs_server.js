/**
 * Interactive Node.js Server Example for AgentShell
 * 
 * This server provides both an HTTP interface and an interactive CLI
 * for demonstration purposes with AgentShell.py
 * 
 * HTTP endpoints:
 * - GET /: Welcome message
 * - GET /echo/{message}: Echo the message
 * 
 * CLI commands:
 * - start [port]: Start the HTTP server
 * - stop: Stop the HTTP server
 * - status: Check server status
 * - help: Display available commands
 * - exit: Exit the program
 * 
 * License: MIT - Use freely for any purpose
 */

const http = require('http');
const readline = require('readline');

// Create HTTP server
const server = http.createServer((req, res) => {
    const url = req.url;

    if (url === '/') {
        res.writeHead(200, { 'Content-Type': 'text/plain' });
        res.end('Welcome to the interactive Node.js server!\n');
    } else if (url.startsWith('/echo/')) {
        const message = url.slice(6);
        res.writeHead(200, { 'Content-Type': 'text/plain' });
        res.end(`Echo: ${message}\n`);
    } else {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('Not Found\n');
    }
});

// Handle server errors
server.on('error', (err) => {
    console.log(`Server error: ${err.message}`);
});

// Set up command line interface
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    prompt: 'server> '
});

// Server state
let port = 3000;
let isRunning = false;

// Handle process errors
process.on('uncaughtException', (err) => {
    if (err.code === 'EPIPE') {
        console.log('EPIPE error caught - pipe was broken');
    } else {
        console.log(`Uncaught exception: ${err.message}`);
    }
});

// Handle commands
rl.on('line', (line) => {
    const input = line.trim();
    const [command, ...args] = input.split(' ');

    try {
        switch (command) {
            case 'start':
                const customPort = parseInt(args[0]);
                if (customPort && !isNaN(customPort)) {
                    port = customPort;
                }

                if (!isRunning) {
                    server.listen(port, () => {
                        console.log(`Server running at http://localhost:${port}/`);
                        isRunning = true;
                    });
                } else {
                    console.log(`Server already running at http://localhost:${port}/`);
                }
                break;

            case 'stop':
                if (isRunning) {
                    server.close(() => {
                        console.log('Server stopped');
                        isRunning = false;
                    });
                } else {
                    console.log('Server is not running');
                }
                break;

            case 'status':
                if (isRunning) {
                    console.log(`Server is running at http://localhost:${port}/`);
                } else {
                    console.log('Server is not running');
                }
                break;

            case 'help':
                console.log('Available commands:');
                console.log('  start [port]  - Start the server (optional port)');
                console.log('  stop          - Stop the server');
                console.log('  status        - Check server status');
                console.log('  help          - Show this help');
                console.log('  exit          - Exit the program');
                break;

            case 'exit':
                if (isRunning) {
                    server.close(() => {
                        console.log('Server stopped');
                        rl.close();
                    });
                } else {
                    rl.close();
                }
                break;

            default:
                console.log(`Unknown command: ${command}`);
                console.log('Type "help" for available commands');
        }
    } catch (err) {
        console.log(`Error processing command: ${err.message}`);
    }

    try {
        rl.prompt();
    } catch (err) {
        if (err.code !== 'EPIPE') {
            console.log(`Prompt error: ${err.message}`);
        }
    }
}).on('close', () => {
    console.log('Exiting server program');
    process.exit(0);
});

// Handle process termination
process.on('SIGINT', () => {
    console.log('Received SIGINT, closing gracefully');
    if (isRunning) {
        server.close();
    }
    process.exit(0);
});

process.on('SIGTERM', () => {
    console.log('Received SIGTERM, closing gracefully');
    if (isRunning) {
        server.close();
    }
    process.exit(0);
});

// Start prompting
console.log('Interactive Node.js Server');
console.log('Type "help" for available commands');
try {
    rl.prompt();
} catch (err) {
    console.log(`Initial prompt error: ${err.message}`);
} 