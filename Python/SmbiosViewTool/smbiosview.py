import os
import re
import sys
from datetime import datetime

def log(msg):
    """Add time to log"""
    timestamp = datetime.now()
    print(f"[{timestamp}] {msg}")

def run_command(cmd):
    """Executes a command using os.system with stdout/stderr muted on screen."""
    return os.system(cmd)

def clean_text(text):
    """
    Removes non-printable ASCII and control characters to prevent file corruption.
    """
    return re.sub(r'[^\x20-\x7E\t\r\n]', '', text)

'''
def format_hex_lines_to_16bytes(raw_hex_lines):
    """
    Extracts raw hex bytes from smbiosview dump and formats them cleanly into 
    16-bytes per line aligned standard Hex Dump (Offset: 16-Bytes | ASCII).
    """
    raw_bytes = bytearray()
    for line in raw_hex_lines:
        if ":" in line:
            content = line.split(":", 1)[1]
        else:
            content = line
        if "*" in content:
            content = content.split("*")[0]
        hex_tokens = re.findall(r'\b[0-9a-fA-F]{2}\b', content)
        for tok in hex_tokens:
            raw_bytes.append(int(tok, 16))
    if not raw_bytes:
        return []
    formatted_output = []
    for offset in range(0, len(raw_bytes), 16):
        chunk = raw_bytes[offset:offset+16]
        hex_str = " ".join(f"{b:02X}" for b in chunk)
        hex_str_padded = f"{hex_str:<47}"
        ascii_str = "".join(chr(b) if 32 <= b <= 126 else "." for b in chunk)
        formatted_output.append(f"{offset:08X}:  {hex_str_padded} |{ascii_str}|")
    return formatted_output
'''

def parse_smbios_type_file(filepath):
    """
    Parses a generated text file from smbiosview.
    """
    table_data = {}
    raw_hex_lines = []
    if not os.path.exists(filepath):
        return [], table_data
    header_ignore_list = [
        "anchor string",
        "eps checksum",
        "entry point len",
        #// "version",
        "number of structures",
        "max struct size",
        "table address",
        "table length",
        "entry point revision",
        "smbios bcd revision",
        "inter anchor",
        "inter checksum"
    ]
    try:
        with open(filepath, "rb") as f:
            raw_bytes = f.read()
        decoded_text = raw_bytes.decode("utf-8", errors="replace")
        cleaned_text = clean_text(decoded_text)
        lines = cleaned_text.splitlines()
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if "enter to continue" in line.lower() or "q to exit" in line.lower():
                continue
            # ===== 新增：處理 "Dump xxx" 開頭的行 =====
            if line.lower().startswith("dump "):
                table_data[line] = ""
                continue
            
            if ":" in line:
                parts = line.split(":", 1)
                key = parts[0].strip()
                val = parts[1].strip()
                
                # 只針對 $Structure Type 移除 $ 前綴
                if key == "$Structure Type":
                    key = "Structure Type"
                
                key_lower = key.lower()
                if any(ignored in key_lower for ignored in header_ignore_list):
                    continue
                if re.match(r'^[0-9a-fA-F]{4,8}\s*:', line) or "hex" in key_lower:
                    raw_hex_lines.append(line)
                elif key and val:
                    table_data[key] = val
            else:
                if re.match(r'^[0-9a-fA-F]{2,}\s+[0-9a-fA-F]{2,}', line):
                    raw_hex_lines.append(line)
    except Exception as e:
        log(f"Error reading file {filepath}: {e}")
    return table_data

def generate_markdown_table(data_dict):
    """Converts a dictionary of key-value pairs to a Markdown table string."""
    if not data_dict:
        return "*No structured data retrieved.*\n"
    md = "| Field Name | Value |\n"
    md += "| :--- | :--- |\n"
    for key, val in data_dict.items():
        clean_key = key.replace("|", "\\|")
        clean_val = val.replace("|", "\\|")
        md += f"| {clean_key} | {clean_val} |\n"
    return md

def main():
    dmi_types = {
        1: "Type 1: System Information",
        2: "Type 2: Baseboard Information",
        3: "Type 3: System Enclosure or Chassis"
    }
    parsed_results = {}
    for t_id, title in dmi_types.items():
        raw_file = f"temp_smbios_t{t_id}.txt"
        cmd = f"smbiosview -t {t_id} > {raw_file}"
        log(f"Executing SMBIOS Type {t_id} query... cmd: {cmd}")
        return_code = run_command(cmd)
        if return_code == 0:
            #//hex_data, table_data = parse_smbios_type_file(raw_file)
            table_data = parse_smbios_type_file(raw_file)
            parsed_results[title] = {
                #//"hex": hex_data,
                "table": table_data
            }
        else:
            log(f"Error: Failed to execute command for Type {t_id}. Return code: {return_code}")
            parsed_results[title] = {"#//hex": [], "table": {}}
    md_filename = "smbios_summary.md"
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    md_content = f"# SMBIOS Information Summary\n"
    for title, content in parsed_results.items():
        md_content += f"## {title}\n\n"
        md_content += generate_markdown_table(content["table"])
        md_content += "\n---\n\n"
    try:
        with open(md_filename, "w", encoding="utf-8") as md_file:
            md_file.write(md_content)
        log(f"Successfully generated Markdown report: {md_filename}")
    except Exception as e:
        log(f"Failed to write Markdown file: {e}")
    for t_id in dmi_types.keys():
        temp_file = f"temp_smbios_t{t_id}.txt"
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except Exception as e:
                log(f"Warning: Could not remove temporary file {temp_file}: {e}")

# === 程式入口：重定向 stdout 到 log 檔 ===
if __name__ == "__main__":
    log_file = open("smbiosview.log", "w", encoding="utf-8")
    sys.stdout = log_file

    #// Don't use this coding style. UEFI python get incorrect value[2]
    #// print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] smbiosview started")
    print(f"[{datetime.now()}] smbiosview started")
    print("=" * 60)

    try:
        main()
    except Exception as e:
        print(f"FATAL: {e}")
    finally:
        print("=" * 60)
        print(f"[{datetime.now()}] smbiosview finished")
        sys.stdout.flush()
        log_file.close()
        sys.stdout = sys.__stdout__