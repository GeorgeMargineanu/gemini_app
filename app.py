from flask import Flask, request, render_template, Response
import subprocess
import pty
import os

app = Flask(__name__, template_folder="templates")

@app.route("/")
def home():
    # Get logo filename from environment variable, default to 'logo.png'
    logo_file = os.getenv("PROJECT_LOGO", "logo.png")
    return render_template("index.html", logo_file=logo_file)

@app.route("/query")
def run_gemini():
    query = request.args.get("query")
    flags = request.args.getlist("flag")  # Accept multiple flags like ?flag=--approval-mode&flag=yolo

    if not query:
        return "No query provided", 400

    # Always include approval-mode yolo for non-interactive execution
    if "--approval-mode" not in flags:
        flags.extend(["--approval-mode", "yolo"])

    cmd = ["gemini", "-p", query] + flags

    def generate():
        # Open pseudo-terminal so Gemini runs like in terminal
        master_fd, slave_fd = pty.openpty()
        process = subprocess.Popen(
            cmd,
            stdout=slave_fd,
            stderr=slave_fd,
            stdin=slave_fd,
            text=True
        )
        os.close(slave_fd)

        # Stream Gemini output line by line
        with os.fdopen(master_fd) as stdout:
            for line in stdout:
                yield f"data: {line}\n\n"

        process.wait()
        yield "data: __DONE__\n\n"

    return Response(generate(), mimetype='text/event-stream')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
