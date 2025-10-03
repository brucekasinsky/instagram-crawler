from flask import Flask, request, jsonify
import time
import pprint
import json
from datetime import datetime
from InstaScraperV2 import ScraperController

app = Flask(__name__)

def scrape_instance(artist_name):
    scraper_instance = ScraperController()
    scraper_instance.create_session()
    
    
    # Autenticação e coleta de dados
    # token_response = scraper_instance.get_token()
    # access_token = token_response['access_token']
    # artist_info = scraper_instance.get_artist_data(artist_name, access_token)
    # artist_id = artist_info['artists']['items'][0]['id']
    # listeners_count = scraper_instance.get_artist_totalplays(artist_id)

    # # Dados do artista principal
    # artist = {
    #     "id": artist_id,
    #     "name": artist_info['artists']['items'][0]['name'],
    #     "link": artist_info['artists']['items'][0]['external_urls']['spotify'],
    #     "monthly_listeners": listeners_count,
    #     "followers": artist_info['artists']['items'][0]['followers']['total'],
    #     "genres": artist_info['artists']['items'][0]['genres'],
    #     "image640": artist_info['artists']['items'][0]['images'][0]['url'],
    #     "image320": artist_info['artists']['items'][0]['images'][1]['url'],
    #     "popularity": artist_info['artists']['items'][0]['popularity']
    # }

    # # Artistas relacionados
    # artist_related_info = scraper_instance.get_artist_related(artist_id, access_token)
    # artist_related = [
    #     {
    #         "id": related['id'],
    #         "name": related['name'],
    #         "link": related['external_urls']['spotify'],
    #         "followers": related['followers']['total'],
    #         "genres": related['genres'],
    #         "image640": related['images'][0]['url'] if related['images'] else None,
    #         "image320": related['images'][1]['url'] if len(related['images']) > 1 else None,
    #         "popularity": related['popularity']
    #     }
    #     for related in artist_related_info['artists'][:5]
    # ]

    # # Álbuns do artista
    # artist_albuns_info = scraper_instance.get_artist_albuns(artist_id, access_token)
    # artist_albuns = [
    #     {
    #         "id": album['id'],
    #         "name": album['name'],
    #         "link": album['external_urls']['spotify'],
    #         "total_tracks": album['total_tracks'],
    #         "album_type": album['album_type'],
    #         "release_date": album['release_date'],
    #         "image640": album['images'][0]['url'] if album['images'] else None,
    #         "image320": album['images'][1]['url'] if len(album['images']) > 1 else None,
    #     }
    #     for album in artist_albuns_info['items']
    # ]

    # # Tracks do artista
    # artist_tracks_info = scraper_instance.get_artist_tracks(artist_id, access_token)
    # artist_tracks = [
    #     {
    #         "id": track['id'],
    #         "name": track['name'],
    #         "link": track['external_urls']['spotify'],
    #         "artists": [artist['name'] for artist in track['artists']],
    #         "duration_ms": track['duration_ms'],
    #         "release_date": track['album']['release_date'],
    #         "image640": track['album']['images'][0]['url'] if track['album']['images'] else None,
    #         "image320": track['album']['images'][1]['url'] if len(track['album']['images']) > 1 else None,
    #         "popularity": track['popularity']
    #     }
    #     for track in artist_tracks_info['tracks']
    # ]

    # return {
    #     "artist": artist,
    #     "artist_related": artist_related,
    #     "artist_albuns": artist_albuns,
    #     "artist_tracks": artist_tracks
    # }

def scrape_reels_instance(profile_name, max_reels=10):
    """
    Função para extrair reels do Instagram usando automação web
    """
    scraper_instance = ScraperController()
    
    try:
        print(f"🎬 Iniciando extração de reels para @{profile_name}...")
        
        # Executar scraper de reels
        result = scraper_instance.scrapper_reels_web(profile_name, max_reels)
        
        return result
        
    except Exception as e:
        print(f"❌ Erro na extração: {str(e)}")
        return {
            'success': 0,
            'message': f'Erro na extração: {str(e)}',
            'data': []
        }
    finally:
        # Fechar navegador
        try:
            scraper_instance.quit_session()
        except:
            pass

@app.route('/scrape_artist', methods=['POST'])
def scrape_artist():
    data = request.get_json()
    artist_name = data.get('artist_name')

    if not artist_name:
        return jsonify({"error": "artist_name is required"}), 400

    try:
        start_time = time.perf_counter()
        result = scrape_instance(artist_name)
        end_time = time.perf_counter()
        return jsonify({
            "data": result,
            "processing_time_seconds": end_time - start_time
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/scrape_reels', methods=['POST'])
def scrape_reels():
    """
    Endpoint para extrair reels do Instagram
    """
    data = request.get_json()
    profile_name = data.get('profile_name')
    max_reels = data.get('max_reels', 10)

    if not profile_name:
        return jsonify({"error": "profile_name is required"}), 400

    try:
        start_time = time.perf_counter()
        result = scrape_reels_instance(profile_name, max_reels)
        end_time = time.perf_counter()
        
        return jsonify({
            "data": result,
            "processing_time_seconds": end_time - start_time,
            "profile": profile_name,
            "max_reels": max_reels
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/login_instagram', methods=['POST'])
def login_instagram():
    """
    Endpoint para fazer login manual no Instagram
    """
    scraper_instance = ScraperController()
    
    try:
        result = scraper_instance.manual_login_instagram()
        
        return jsonify({
            "success": result,
            "message": "Login realizado com sucesso" if result else "Falha no login"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        try:
            scraper_instance.quit_session()
        except:
            pass

def run_cli():
    """
    Sistema automático para extração de reels do Instagram
    """
    print("🎬 SISTEMA AUTOMÁTICO DE EXTRAÇÃO DE REELS")
    print("=" * 60)
    print("📝 Este sistema irá:")
    print("   1. 🚀 Abrir o navegador Chrome automaticamente")
    print("   2. 🔐 Permitir login manual no Instagram")
    print("   3. 🎬 Extrair reels automaticamente do perfil 'instagram'")
    print("=" * 60)
    
    # Criar instância do scraper
    scraper = ScraperController()
    
    try:
        # PASSO 1: ABRIR SELENIUM E FAZER LOGIN
        print("\n🚀 ABRINDO NAVEGADOR E FAZENDO LOGIN...")
        print("=" * 50)
        
        if not scraper.manual_login_instagram():
            print("❌ Falha no login. Sistema encerrado.")
            return
        
        print("✅ Login realizado com sucesso!")
        
        # PASSO 2: EXTRAÇÃO AUTOMÁTICA
        print("\n🎬 INICIANDO EXTRAÇÃO AUTOMÁTICA...")
        print("=" * 50)
        
        # Configuração automática (pode ser sobrescrita por argumentos)
        import sys
        profile_name = "felipeneto"  # Perfil padrão
        max_reels = 20  # Quantidade padrão
        
        # Verificar se foi passado perfil como argumento
        if len(sys.argv) > 2:
            profile_name = sys.argv[2]
        if len(sys.argv) > 3:
            try:
                max_reels = int(sys.argv[3])
            except ValueError:
                max_reels = 20
        
        print(f"🎯 Configuração automática:")
        print(f"   👤 Perfil: @{profile_name}")
        print(f"   📊 Máximo de reels: {max_reels}")
        print("   🤖 Modo: TOTALMENTE AUTOMÁTICO")
        
        # PASSO 3: EXTRAIR REELS AUTOMATICAMENTE
        print(f"\n🚀 EXTRAINDO REELS DE @{profile_name} AUTOMATICAMENTE...")
        print("=" * 50)
        
        # Executar scraper automaticamente
        result = scraper.scrapper_reels_web(profile_name, max_reels)
        
        # PASSO 4: EXIBIR RESULTADOS AUTOMATICAMENTE
        print(f"\n📊 RESULTADOS DA EXTRAÇÃO:")
        print("=" * 50)
        
        if result['success'] == 1:
            data = result['data']
            print(f"✅ Status: {result['message']}")
            print(f"👤 Perfil: @{data['profile']}")
            print(f"🎬 Total de reels: {data['total_reels']}")
            
            if data['statistics']:
                stats = data['statistics']
                print(f"❤️ Total de likes: {stats['total_likes']:,}")
                print(f"💬 Total de comentários: {stats['total_comments']:,}")
                print(f"📈 Média de likes: {stats['average_likes']:,}")
                print(f"📈 Média de comentários: {stats['average_comments']:,}")
            
            # Salvar resultados automaticamente
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"reels_{profile_name}_{timestamp}.json"
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                
                print(f"\n💾 Resultados salvos automaticamente em: {filename}")
                
            except Exception as e:
                print(f"⚠️ Erro ao salvar resultados: {str(e)}")
                
            print(f"\n🎉 EXTRAÇÃO CONCLUÍDA COM SUCESSO!")
            print(f"📊 {data['total_reels']} reels extraídos de @{profile_name}")
        else:
            print(f"❌ Erro na extração: {result['message']}")
        
    except KeyboardInterrupt:
        print("\n⚠️ Sistema interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # Fechar navegador automaticamente
        print("\n🔒 Fechando navegador automaticamente...")
        scraper.quit_session()
        print("✅ Sistema finalizado!")

if __name__ == '__main__':
    import sys
    
    # Verificar se foi chamado com argumentos para CLI
    if len(sys.argv) > 1 and sys.argv[1] == 'cli':
        run_cli()
    else:
        # Executar como servidor Flask
        print("🌐 Iniciando servidor Flask...")
        print("📝 Para sistema automático use:")
        print("   python main.py cli                    # Extrair reels de @instagram")
        print("   python main.py cli nasa               # Extrair reels de @nasa")
        print("   python main.py cli nasa 15            # Extrair 15 reels de @nasa")
        print("🔗 Endpoints API disponíveis:")
        print("   POST /scrape_reels - Extrair reels do Instagram")
        print("   POST /login_instagram - Fazer login manual")
        print("   POST /scrape_artist - Extrair dados de artista (Spotify)")
        print("=" * 50)
        app.run(debug=True, host="0.0.0.0", port=8080)
