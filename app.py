from flask import Flask, request, send_from_directory, Response
import subprocess
import sys

app = Flask(__name__)

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/query")
def run_gemini():
    query = request.args.get("query")
    if not query:
        return "No query provided", 400

    def generate():
        process = subprocess.Popen(
            ["gemini", "-p", query],  # Add flags if gemini supports unbuffered output
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1  # line-buffered
        )
        for line in iter(process.stdout.readline, ''):
            yield f"data: {line}\n\n"
            sys.stdout.flush()  # flush for SSE
        process.stdout.close()
        process.wait()
        yield "data __DONE__\n\n" # Marker to signal frontent that the streaming finished

    return Response(generate(), mimetype='text/event-stream')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)