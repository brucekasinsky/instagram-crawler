"""
Main entry point for Instagram Scraper
Replicates the functionality of indexdados.php
"""
import json
import sys
from typing import Dict, Any
from instagram_scraper import InstagramScraper

def escape_json_string(value: str) -> str:
    """Escape JSON string (replicates PHP function)"""
    escapers = ['\\"']
    replacements = ['"']
    result = value
    for escaper, replacement in zip(escapers, replacements):
        result = result.replace(escaper, replacement)
    return result

def main():
    """Main function that replicates indexdados.php behavior"""
    
    # Set default JSON input (for testing, same as PHP version)
    json_input = '{"instagramuser":"felipeneto"}'
    
    # In production, you would read from stdin or HTTP request
    # json_input = sys.stdin.read()
    
    try:
        # Parse JSON input
        post_data = json.loads(json_input.strip())
        instagram_user = post_data.get('instagramuser', '')
        
        if not instagram_user:
            result = {
                'success': 0,
                'message': 'Instagram user not provided',
                'data': []
            }
        else:
            # Initialize scraper
            scraper = InstagramScraper()
            
            # Scrape user data
            result = scraper.scrape_user(instagram_user)
        
        # Process result (same logic as PHP version)
        processed_result = escape_json_string(json.dumps(result, ensure_ascii=False))
        
        # Handle single object vs array (same as PHP logic)
        if processed_result.startswith('{'):
            final_result = [result]
        else:
            final_result = result
        
        # Output JSON response
        print(json.dumps(final_result, ensure_ascii=False, indent=2))
        
    except json.JSONDecodeError as e:
        error_result = {
            'success': 0,
            'message': f'Invalid JSON input: {str(e)}',
            'data': []
        }
        print(json.dumps([error_result], ensure_ascii=False, indent=2))
        
    except Exception as e:
        error_result = {
            'success': 0,
            'message': f'Unexpected error: {str(e)}',
            'data': []
        }
        print(json.dumps([error_result], ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
