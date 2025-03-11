import instaloader
import datetime
import pandas as pd
import os
import argparse
from tqdm import tqdm
import time
import getpass

def scrape_instagram_posts(username, limit=None, output_format='csv', login_user=None, delay=2):
    """
    Scrape Instagram posts from a specific user and save the results with posting time and scraping time.
    
    Args:
        username (str): Instagram username to scrape
        limit (int, optional): Maximum number of posts to scrape. None means all posts.
        output_format (str, optional): Output format ('csv' or 'excel'). Defaults to 'csv'.
        login_user (str, optional): Instagram username to login with. If None, no login is performed.
        delay (int, optional): Delay in seconds between requests to avoid rate limiting. Defaults to 2.
    
    Returns:
        str: Path to the saved file
    """
    # Inisialisasi instaloader
    L = instaloader.Instaloader()
    
    # Login ke Instagram jika username login diberikan
    if login_user:
        try:
            password = getpass.getpass(f"Masukkan password untuk {login_user}: ")
            print(f"Mencoba login sebagai {login_user}...")
            L.login(login_user, password)
            print("Login berhasil!")
        except Exception as e:
            print(f"Login gagal: {str(e)}")
            print("Melanjutkan tanpa login...")
    
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
                
            # Tambahkan delay untuk menghindari rate limiting
            time.sleep(delay)
        
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
    except instaloader.exceptions.ConnectionException as e:
        print(f"Error koneksi: {str(e)}")
        print("Saran: Tunggu beberapa menit dan coba lagi, atau gunakan VPN untuk mengubah IP Anda.")
    except instaloader.exceptions.LoginRequiredException:
        print("Error: Login diperlukan untuk mengakses data ini.")
        print("Saran: Jalankan script dengan parameter login_user untuk login ke Instagram.")
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Saran: Jika error berkaitan dengan rate limiting, tunggu beberapa menit dan coba lagi.")
    
    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape Instagram posts with posting time and scraping time')
    parser.add_argument('username', type=str, help='Instagram username to scrape')
    parser.add_argument('--limit', type=int, default=None, help='Maximum number of posts to scrape')
    parser.add_argument('--format', type=str, choices=['csv', 'excel'], default='csv', help='Output format (csv or excel)')
    parser.add_argument('--login', type=str, default=None, help='Instagram username to login with')
    parser.add_argument('--delay', type=int, default=2, help='Delay in seconds between requests to avoid rate limiting')
    
    args = parser.parse_args()
    
    scrape_instagram_posts(args.username, args.limit, args.format, args.login, args.delay) 