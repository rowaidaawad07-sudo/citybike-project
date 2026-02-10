"""
Umfassende Testsuite für das CityBike-Projekt.
Testet die Modelle, Factories und Pricing-Strategien.
"""

import sys
import os
from datetime import datetime

# Füge den citybike-Ordner zum Python-Pfad hinzu
current_dir = os.path.dirname(os.path.abspath(__file__))
citybike_path = os.path.join(current_dir, 'citybike')

if os.path.exists(citybike_path):
    sys.path.insert(0, citybike_path)
    print(f"✅ Pfad hinzugefügt: {citybike_path}")
else:
    print(f"❌ FEHLER: 'citybike'-Ordner nicht gefunden in: {current_dir}")
    sys.exit(1)

print("="*60)
print("🚀 CITYBIKE TESTSUITE - HAUPTPROJEKT")
print("="*60)
print(f"📁 Arbeitsverzeichnis: {current_dir}")
print(f"📦 CityBike-Pfad: {citybike_path}")

# Prüfe, ob die benötigten Dateien im citybike-Ordner existieren
print("\n🔍 Prüfe Dateien im citybike-Ordner:")
required_files = ['models.py', 'factories.py', 'pricing.py', 'analyzer.py']
all_files_exist = True

for file in required_files:
    file_path = os.path.join(citybike_path, file)
    if os.path.exists(file_path):
        size = os.path.getsize(file_path)
        print(f"✅ {file} gefunden ({size} Bytes)")
    else:
        print(f"❌ {file} NICHT gefunden!")
        all_files_exist = False

if not all_files_exist:
    print("\n❌ Kritische Dateien fehlen. Test wird abgebrochen.")
    sys.exit(1)

try:
    print("\n🔄 Importiere Module...")
    
    # Importiere aus dem citybike-Ordner
    from models import (
        Bike, ClassicBike, ElectricBike,
        Station, CasualUser, MemberUser,
        Trip, MaintenanceRecord
    )
    print("✅ models.py importiert")
    
    from factories import (
        create_bike, create_user, create_station,
        create_trip, create_maintenance_record
    )
    print("✅ factories.py importiert")
    
    from pricing import (
        CasualPricing, MemberPricing, PeakHourPricing
    )
    print("✅ pricing.py importiert")
    
    from analyzer import BikeShareSystem
    print("✅ analyzer.py importiert")
    
    print("\n🎉 Alle Module erfolgreich importiert!")
    
except ImportError as e:
    print(f"\n❌ Import-Fehler: {e}")
    print("\n🔧 Mögliche Lösungen:")
    print("1. Prüfen Sie, ob die Dateien im 'citybike' Ordner sind")
    print("2. Prüfen Sie die Syntax der Dateien")
    print("3. Prüfen Sie, ob alle Klassen korrekt definiert sind")
    
    # Zeige den Traceback für genauere Diagnose
    import traceback
    traceback.print_exc()
    sys.exit(1)

# -------------------------------------------------------------------
# VEREINFACHTE TESTFUNKTIONEN
# -------------------------------------------------------------------

def einfacher_bike_test():
    """Einfacher Test für die Bike-Hierarchie."""
    try:
        print("\n1️⃣ TEST: Bike-Hierarchie")
        cb = ClassicBike("TEST-001", gear_count=7)
        print(f"   ✅ ClassicBike: {cb}")
        
        eb = ElectricBike("TEST-002", battery_level=85.5)
        print(f"   ✅ ElectricBike: {eb}")
        return True
    except Exception as e:
        print(f"   ❌ Fehler: {e}")
        return False

def einfacher_station_test():
    """Einfacher Test für Station."""
    try:
        print("\n2️⃣ TEST: Station")
        st = Station("ST-TEST", "Test Station", 20, 52.52, 13.40)
        print(f"   ✅ Station: {st}")
        return True
    except Exception as e:
        print(f"   ❌ Fehler: {e}")
        return False

def einfacher_user_test():
    """Einfacher Test für User-Hierarchie."""
    try:
        print("\n3️⃣ TEST: User-Hierarchie")
        cu = CasualUser("U-TEST", "Max Mustermann", "max@test.de")
        print(f"   ✅ CasualUser: {cu}")
        
        mu = MemberUser("M-TEST", "Lisa Mitglied", "lisa@test.de", tier="premium")
        print(f"   ✅ MemberUser: {mu}")
        return True
    except Exception as e:
        print(f"   ❌ Fehler: {e}")
        return False

def einfacher_factory_test():
    """Einfacher Test für Factory Pattern."""
    try:
        print("\n4️⃣ TEST: Factory Pattern")
        
        # Bike Factory
        bike_data = {"bike_id": "F-BIKE", "bike_type": "classic", "gear_count": "5"}
        bike = create_bike(bike_data)
        print(f"   ✅ Bike Factory: {bike}")
        
        # User Factory
        user_data = {"user_id": "F-USER", "name": "Factory User", "user_type": "casual"}
        user = create_user(user_data)
        print(f"   ✅ User Factory: {user}")
        
        return True
    except Exception as e:
        print(f"   ❌ Fehler: {e}")
        return False

def einfacher_pricing_test():
    """Einfacher Test für Pricing Strategy."""
    try:
        print("\n5️⃣ TEST: Pricing Strategy")
        
        cp = CasualPricing()
        cost_casual = cp.calculate_cost(10, 2)
        print(f"   ✅ CasualPricing: 10min, 2km = €{cost_casual:.2f}")
        
        mp = MemberPricing()
        cost_member = mp.calculate_cost(10, 2)
        print(f"   ✅ MemberPricing: 10min, 2km = €{cost_member:.2f}")
        
        return True
    except Exception as e:
        print(f"   ❌ Fehler: {e}")
        return False

def einfacher_analyzer_test():
    """Einfacher Test für Analyzer."""
    try:
        print("\n6️⃣ TEST: Analyzer")
        system = BikeShareSystem()
        print(f"   ✅ BikeShareSystem instanziiert")
        
        # Prüfe, ob wichtige Methoden existieren
        methods = ['load_data', 'clean_data', 'total_trips_summary']
        for method in methods:
            if hasattr(system, method):
                print(f"   ✅ Methode '{method}' vorhanden")
            else:
                print(f"   ❌ Methode '{method}' fehlt")
        
        return True
    except Exception as e:
        print(f"   ❌ Fehler: {e}")
        return False

# -------------------------------------------------------------------
# HAUPTFUNKTION
# -------------------------------------------------------------------

def run_einfache_tests():
    """Führt alle vereinfachten Tests aus."""
    
    print("\n" + "="*60)
    print("🧪 STARTE VEREINFACHTE TESTS")
    print("="*60)
    
    tests = [
        ("Bike-Hierarchie", einfacher_bike_test),
        ("Station", einfacher_station_test),
        ("User-Hierarchie", einfacher_user_test),
        ("Factory Pattern", einfacher_factory_test),
        ("Pricing Strategy", einfacher_pricing_test),
        ("Analyzer", einfacher_analyzer_test),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ Unerwarteter Fehler in {test_name}: {e}")
            results.append((test_name, False))
    
    # Zusammenfassung
    print("\n" + "="*60)
    print("📊 ZUSAMMENFASSUNG")
    print("="*60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ BESTANDEN" if success else "❌ FEHLGESCHLAGEN"
        print(f"{status}: {test_name}")
    
    print(f"\n📈 ERGEBNIS: {passed}/{total} Tests bestanden")
    
    if passed == total:
        print("\n🎉 HERZLICHEN GLÜCKWUNSCH!")
        print("Alle grundlegenden Tests bestanden!")
        print("\nIhr Projekt ist grundlegend funktionsfähig.")
        print("Sie können nun mit den restlichen Teilen fortfahren:")
        print("  - algorithms.py (Sortieren & Suchen)")
        print("  - numerical.py (NumPy-Berechnungen)")
        print("  - visualization.py (Diagramme)")
        print("  - main.py (Hauptprogramm)")
        return True
    else:
        print(f"\n⚠️  {total - passed} Test(s) fehlgeschlagen.")
        print("Bitte überprüfen Sie die fehlgeschlagenen Komponenten.")
        return False

# -------------------------------------------------------------------
# START
# -------------------------------------------------------------------

if __name__ == "__main__":
    try:
        success = run_einfache_tests()
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Test abgebrochen.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ KRITISCHER FEHLER: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)