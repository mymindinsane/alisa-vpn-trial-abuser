import threading
import tkinter as tk
from tkinter import messagebox, ttk
from types import SimpleNamespace

from register_vpn_link import default_settings, run_registration_flow


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("VPN Link")
        self.geometry("760x560")
        self.minsize(680, 500)

        self.settings = default_settings()
        self.link_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready")
        self.headful_var = tk.BooleanVar(value=self.settings.headful)
        self.browser_channel_var = tk.StringVar(value=self.settings.browser_channel)
        self.download_chromium_var = tk.BooleanVar(value=self.settings.download_chromium_if_needed)

        self.inputs = {}

        self._build_ui()

    def _build_ui(self):
        root = ttk.Frame(self, padding=16)
        root.pack(fill="both", expand=True)

        title = ttk.Label(root, text="VPN Link", font=("Segoe UI", 18, "bold"))
        title.pack(anchor="w")

        form = ttk.LabelFrame(root, text="Settings", padding=12)
        form.pack(fill="x", pady=(14, 10))

        self._add_input(form, "URL", "url", self.settings.url, 0)
        self._add_input(form, "Password", "password", self.settings.password, 1, show="*")
        self._add_input(form, "Email prefix", "email_prefix", self.settings.email_prefix, 2)
        self._add_input(form, "Email domain", "email_domain", self.settings.email_domain, 3)
        self._add_input(form, "Device text", "device_text", self.settings.device_text, 4)
        self._add_input(form, "Timeout ms", "timeout_ms", str(self.settings.timeout_ms), 5)
        self._add_input(form, "Link selector", "link_selector", self.settings.link_selector or "", 6)

        ttk.Label(form, text="Browser").grid(row=7, column=0, sticky="w", padx=(0, 10), pady=4)
        browser = ttk.Combobox(
            form,
            textvariable=self.browser_channel_var,
            values=("auto", "msedge", "chrome", "chromium"),
            state="readonly",
        )
        browser.grid(row=7, column=1, sticky="ew", pady=4)

        headful = ttk.Checkbutton(form, text="Show browser window", variable=self.headful_var)
        headful.grid(row=8, column=1, sticky="w", pady=(8, 0))

        download = ttk.Checkbutton(form, text="Download Chromium if needed", variable=self.download_chromium_var)
        download.grid(row=9, column=1, sticky="w", pady=(4, 0))

        form.columnconfigure(1, weight=1)

        actions = ttk.Frame(root)
        actions.pack(fill="x", pady=(0, 10))

        self.start_button = ttk.Button(actions, text="Start", command=self.start_flow)
        self.start_button.pack(side="left")

        self.copy_button = ttk.Button(actions, text="Copy link", command=self.copy_link, state="disabled")
        self.copy_button.pack(side="left", padx=(8, 0))

        status = ttk.Label(actions, textvariable=self.status_var)
        status.pack(side="right")

        result = ttk.LabelFrame(root, text="Result", padding=12)
        result.pack(fill="x", pady=(0, 10))

        ttk.Label(result, text="Generated email").grid(row=0, column=0, sticky="w", padx=(0, 10))
        ttk.Entry(result, textvariable=self.email_var, state="readonly").grid(row=0, column=1, sticky="ew")

        ttk.Label(result, text="Link").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=(8, 0))
        ttk.Entry(result, textvariable=self.link_var, state="readonly").grid(row=1, column=1, sticky="ew", pady=(8, 0))

        result.columnconfigure(1, weight=1)

        log_frame = ttk.LabelFrame(root, text="Log", padding=8)
        log_frame.pack(fill="both", expand=True)

        self.log_box = tk.Text(log_frame, height=10, wrap="word", state="disabled")
        self.log_box.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_box.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_box.configure(yscrollcommand=scrollbar.set)

    def _add_input(self, parent, label, key, value, row, show=None):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", padx=(0, 10), pady=4)
        var = tk.StringVar(value=value)
        entry = ttk.Entry(parent, textvariable=var, show=show)
        entry.grid(row=row, column=1, sticky="ew", pady=4)
        self.inputs[key] = var

    def build_settings(self):
        settings = default_settings()

        settings.url = self.inputs["url"].get().strip()
        settings.password = self.inputs["password"].get()
        settings.email_prefix = self.inputs["email_prefix"].get().strip()
        settings.email_domain = self.inputs["email_domain"].get().strip()
        settings.device_text = self.inputs["device_text"].get().strip()
        settings.browser_channel = self.browser_channel_var.get()
        settings.download_chromium_if_needed = self.download_chromium_var.get()
        settings.headful = self.headful_var.get()
        settings.link_selector = self.inputs["link_selector"].get().strip() or None

        timeout_raw = self.inputs["timeout_ms"].get().strip()
        try:
            settings.timeout_ms = int(timeout_raw)
        except ValueError:
            raise ValueError("Timeout must be a number.")

        return settings

    def start_flow(self):
        try:
            settings = self.build_settings()
        except ValueError as exc:
            messagebox.showerror("Invalid settings", str(exc))
            return

        self.start_button.configure(state="disabled")
        self.copy_button.configure(state="disabled")
        self.email_var.set("")
        self.link_var.set("")
        self.status_var.set("Running...")
        self.clear_log()

        worker = threading.Thread(target=self.run_worker, args=(settings,), daemon=True)
        worker.start()

    def run_worker(self, settings: SimpleNamespace):
        try:
            email, link = run_registration_flow(settings, log=self.log)
            self.after(0, self.finish_success, email, link)
        except Exception as exc:
            self.after(0, self.finish_error, exc)

    def finish_success(self, email, link):
        self.email_var.set(email)
        self.link_var.set(link)
        self.status_var.set("Done")
        self.copy_button.configure(state="normal")
        self.start_button.configure(state="normal")
        self.log("Done.")

    def finish_error(self, exc):
        self.status_var.set("Failed")
        self.start_button.configure(state="normal")
        self.log(f"Failed: {exc}")
        messagebox.showerror("Failed", str(exc))

    def copy_link(self):
        link = self.link_var.get()
        if not link:
            return

        self.clipboard_clear()
        self.clipboard_append(link)
        self.status_var.set("Link copied")

    def clear_log(self):
        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.configure(state="disabled")

    def log(self, message):
        self.after(0, self._append_log, message)

    def _append_log(self, message):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"{message}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")


if __name__ == "__main__":
    App().mainloop()
