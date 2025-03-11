import instaloader
import datetime
import pandas as pd
import os
import argparse
from tqdm import tqdm

def scrape_instagram_posts(username, limit=None, output_format='csv'):
    """
    Scrape Instagram posts from a specific user and save the results with posting time and scraping time.
    
    Args:
        username (str): Instagram username to scrape
        limit (int, optional): Maximum number of posts to scrape. None means all posts.
        output_format (str, optional): Output format ('csv' or 'excel'). Defaults to 'csv'.
    
    Returns:
        str: Path to the saved file
    """
    # Inisialisasi instaloader
    L = instaloader.Instaloader()
    
    # Waktu scraping
    scrape_time = datetime.datetime.now()
    scrape_time_str = scrape_time.strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        # Dapatkan profil
        profile = instaloader.Profile.from_username(L.context, username)
        
        # Siapkan list untuk menyimpan data
        posts_data = []
        
        # Iterasi melalui post
        print(f"Scraping posts dari {username}...")
        posts_iterator = profile.get_posts()
        
        # Jika limit ditentukan, batasi jumlah post
        if limit:
            posts_iterator = list(posts_iterator)[:limit]
            
        for post in tqdm(posts_iterator):
            post_data = {
                'post_id': post.shortcode,
                'post_url': f"https://www.instagram.com/p/{post.shortcode}/",
                'caption': post.caption if post.caption else "",
                'likes': post.likes,
                'comments': post.comments,
                'posting_time': post.date_local.strftime("%Y-%m-%d %H:%M:%S"),
                'scraping_time': scrape_time_str,
                'is_video': post.is_video,
                'location': post.location.name if post.location else None,
                'hashtags': ", ".join(post.caption_hashtags) if post.caption_hashtags else ""
            }
            posts_data.append(post_data)
            
            if limit and len(posts_data) >= limit:
                break
        
        # Buat DataFrame
        df = pd.DataFrame(posts_data)
        
        # Buat direktori output jika belum ada
        os.makedirs('instagram_data', exist_ok=True)
        
        # Simpan hasil
        timestamp = scrape_time.strftime("%Y%m%d_%H%M%S")
        if output_format.lower() == 'excel':
            output_path = f"instagram_data/{username}_posts_{timestamp}.xlsx"
            df.to_excel(output_path, index=False)
        else:  # default to csv
            output_path = f"instagram_data/{username}_posts_{timestamp}.csv"
            df.to_csv(output_path, index=False)
            
        print(f"Berhasil scraping {len(posts_data)} posts dari {username}")
        print(f"Data disimpan di: {output_path}")
        return output_path
        
    except instaloader.exceptions.ProfileNotExistsException:
        print(f"Error: Profil '{username}' tidak ditemukan.")
    except Exception as e:
        print(f"Error: {str(e)}")
    
    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape Instagram posts with posting time and scraping time')
    parser.add_argument('username', type=str, help='Instagram username to scrape')
    parser.add_argument('--limit', type=int, default=None, help='Maximum number of posts to scrape')
    parser.add_argument('--format', type=str, choices=['csv', 'excel'], default='csv', help='Output format (csv or excel)')
    
    args = parser.parse_args()
    
    scrape_instagram_posts(args.username, args.limit, args.format) 