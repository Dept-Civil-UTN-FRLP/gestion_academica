from django.core.management.utils import get_random_secret_key

def generate_secret_key():
    """Genera una nueva SECRET_KEY segura para Django"""
    secret_key = get_random_secret_key()
    print("Tu nueva SECRET_KEY es:")
    print(secret_key)
    print("\nCópiala y pégala en tu archivo .env")
    return secret_key


if __name__ == '__main__':
    generate_secret_key()
