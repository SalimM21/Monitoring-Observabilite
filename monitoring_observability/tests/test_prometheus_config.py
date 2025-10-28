import yaml
import sys

PROMETHEUS_CONFIG_PATH = "prometheus.yml"

def validate_prometheus_config(config_path):
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        # Vérifications basiques
        if "global" not in config:
            print("❌ Erreur : section 'global' manquante")
            return False

        if "scrape_configs" not in config:
            print("❌ Erreur : section 'scrape_configs' manquante")
            return False

        for scrape in config["scrape_configs"]:
            if "job_name" not in scrape:
                print("❌ Erreur : 'job_name' manquant dans un scrape_config")
                return False
            if "static_configs" not in scrape:
                print(f"❌ Erreur : 'static_configs' manquant pour job {scrape['job_name']}")
                return False

        print("✅ Configuration Prometheus valide !")
        return True

    except yaml.YAMLError as e:
        print(f"❌ Erreur YAML : {e}")
        return False
    except FileNotFoundError:
        print(f"❌ Fichier non trouvé : {config_path}")
        return False

if __name__ == "__main__":
    if not validate_prometheus_config(PROMETHEUS_CONFIG_PATH):
        sys.exit(1)
