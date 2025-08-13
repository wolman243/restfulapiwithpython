import subprocess
import json

def run_katana_crawl(target_url):
    try:
        cmd = [ "docker", "exec", "katana_crawler",
            "katana", "-u", target_url, "-silent", "-jsonl" ]
        
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)

        urls = []

        for line in result.strip().split("\n"):

            try:
                data = json.loads(line)
                urls.append(data.get("url"))

            except json.JSONDecodeError:
                pass

        return {
            "status": "success",
            "target": target_url,
            "url_count": len(urls),
             }
    
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": e.output}