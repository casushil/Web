import re
from datetime import datetime, timedelta

def parse_timestamp(timestamp):
    """Convert SRT timestamp to timedelta object"""
    time_pattern = r'(\d{2}):(\d{2}):(\d{2}),(\d{3})'
    match = re.match(time_pattern, timestamp)
    if not match:
        raise ValueError(f"Invalid timestamp format: {timestamp}")
    
    hours, minutes, seconds, milliseconds = map(int, match.groups())
    return timedelta(
        hours=hours,
        minutes=minutes,
        seconds=seconds,
        milliseconds=milliseconds
    )

def format_timestamp(td):
    """Convert timedelta to SRT timestamp format"""
    total_seconds = td.total_seconds()
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    milliseconds = int((total_seconds * 1000) % 1000)
    
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def delay_timestamps(input_file, output_file, delay_seconds):
    """
    Read an SRT file and write a new one with adjusted timestamps
    
    Args:
        input_file (str): Path to input SRT file
        output_file (str): Path to output SRT file
        delay_seconds (float): Number of seconds to subtract from timestamps
    """
    delay = timedelta(seconds=delay_seconds)
    timestamp_pattern = r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})'
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    def replace_timestamps(match):
        start_time = parse_timestamp(match.group(1))
        end_time = parse_timestamp(match.group(2))
        
        # Subtract the delay (with floor at 00:00:00,000)
        new_start = format_timestamp(max(start_time - delay, timedelta()))
        new_end = format_timestamp(max(end_time - delay, timedelta()))
        
        return f"{new_start} --> {new_end}"
    
    adjusted_content = re.sub(timestamp_pattern, replace_timestamps, content)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(adjusted_content)

def main():
    # Example usage
    input_file = "input.srt"
    output_file = "output_adjusted.srt"
    delay_seconds = 12.80  # Will be subtracted from timestamps
    
    try:
        delay_timestamps(input_file, output_file, delay_seconds)
        print(f"Successfully adjusted subtitles backward by {delay_seconds} seconds")
        print(f"Output written to: {output_file}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()