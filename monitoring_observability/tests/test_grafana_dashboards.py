import os
import json
import sys

# Dossier contenant les dashboards JSON
DASHBOARD_DIR = "grafana/dashboards"

def validate_dashboard_json(file_path):
    try:
        with open(file_path, "r") as f:
            json.load(f)
        print(f"✅ Dashboard valide : {file_path}")
        return True
    except json.JSONDecodeError as e:
        print(f"❌ Erreur JSON dans {file_path} : {e}")
        return False
    except FileNotFoundError:
        print(f"❌ Fichier non trouvé : {file_path}")
        return False

def main():
    if not os.path.exists(DASHBOARD_DIR):
        print(f"❌ Dossier dashboards introuvable : {DASHBOARD_DIR}")
        sys.exit(1)

    all_valid = True
    for filename in os.listdir(DASHBOARD_DIR):
        if filename.endswith(".json"):
            file_path = os.path.join(DASHBOARD_DIR, filename)
            if not validate_dashboard_json(file_path):
                all_valid = False

    if all_valid:
        print("✅ Tous les dashboards sont valides !")
        sys.exit(0)
    else:
        print("❌ Certains dashboards contiennent des erreurs")
        sys.exit(1)

if __name__ == "__main__":
    main()
