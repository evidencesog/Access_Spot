import subprocess
import signal
import time
from pathlib import Path
from rich.console import Console

console = Console()

HOSTAPD_CONFIG = Path(__file__).parent / "hostapd.conf"
hostapd_process = None

def start_hostapd():
    global hostapd_process
    if not HOSTAPD_CONFIG.exists():
        console.print("[red]Hostapd config file not found![/red]")
        return

    console.print("[green]Starting Hostapd...[/green]")
    hostapd_process = subprocess.Popen(
        ["sudo", "hostapd", str(HOSTAPD_CONFIG)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(2)
    if hostapd_process.poll() is None:
        console.print("[bold green]Hotspot is running![/bold green]")
    else:
        console.print("[bold red]Hostapd failed to start.[/bold red]")

def stop_hostapd():
    global hostapd_process
    if hostapd_process:
        console.print("[yellow]Stopping Hostapd...[/yellow]")
        hostapd_process.send_signal(signal.SIGTERM)
        hostapd_process.wait()
        console.print("[bold yellow]Hostapd stopped.[/bold yellow]")
    else:
        console.print("[red]Hostapd is not running.[/red]")

def show_connected_devices():
    console.print("[cyan]Fetching connected devices...[/cyan]")
    try:
        result = subprocess.run(
            ["sudo", "iw", "dev", "wlan0", "station", "dump"],
            capture_output=True, text=True
        )
        console.print(result.stdout if result.stdout else "[yellow]No devices connected[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

if __name__ == "__main__":
    console.print("[bold]Python Hostapd Controller[/bold]")
    start_hostapd()
    try:
        while True:
            time.sleep(10)
            show_connected_devices()
    except KeyboardInterrupt:
        stop_hostapd()
