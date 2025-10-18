#!/usr/bin/env python3
"""
ALORIA AGENCY CRM - Générateur de données de test
Script complet pour tester le formulaire de contact et le CRM dans toutes les vues
"""

import requests
import json
import random
from datetime import datetime, timedelta
import os
import time
from typing import List, Dict

# Configuration
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://aloria-prospect.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

class CRMDataGenerator:
    def __init__(self):
        self.session = requests.Session()
        self.manager_token = None
        self.employee_token = None
        self.created_messages = []
        
    def login_manager(self):
        """Connexion Manager"""
        print("🔐 Connexion Manager...")
        login_data = {
            "email": "manager@test.com", 
            "password": "password123"
        }
        
        response = self.session.post(f"{API_BASE}/auth/login", json=login_data)
        if response.status_code == 200:
            self.manager_token = response.json()['access_token']
            print("✅ Manager connecté avec succès")
            return True
        else:
            print(f"❌ Échec connexion Manager: {response.status_code}")
            return False
    
    def create_employee_for_testing(self):
        """Créer un employé pour les tests"""
        if not self.manager_token:
            return False
            
        print("👤 Création employé de test...")
        headers = {"Authorization": f"Bearer {self.manager_token}"}
        
        employee_data = {
            "email": "employee.test@aloria.com",
            "full_name": "Marie Dubois",
            "role": "EMPLOYEE"
        }
        
        response = self.session.post(f"{API_BASE}/users", json=employee_data, headers=headers)
        if response.status_code in [200, 201]:
            print("✅ Employé de test créé")
            
            # Login employé
            login_data = {
                "email": "employee.test@aloria.com",
                "password": "Aloria2024!"
            }
            
            login_response = self.session.post(f"{API_BASE}/auth/login", json=login_data)
            if login_response.status_code == 200:
                self.employee_token = login_response.json()['access_token']
                print("✅ Employé connecté")
                return True
        
        print("⚠️ Employé peut-être déjà existant, tentative de connexion...")
        login_data = {
            "email": "employee.test@aloria.com",
            "password": "Aloria2024!"
        }
        
        login_response = self.session.post(f"{API_BASE}/auth/login", json=login_data)
        if login_response.status_code == 200:
            self.employee_token = login_response.json()['access_token']
            print("✅ Employé connecté (existant)")
            return True
        
        return False

    def get_sample_contact_data(self) -> List[Dict]:
        """Générateur de données de contact réalistes"""
        
        # Profils variés avec différents scores de lead
        profiles = [
            {
                "name": "Jean-Pierre Martin",
                "email": "jp.martin@gmail.com",
                "phone": "+33 6 12 34 56 78",
                "country": "France",
                "visa_type": "Permis de Travail (Passeport Talent)",
                "budget_range": "5000+€",
                "urgency_level": "URGENT",
                "message": "Ingénieur informatique avec 8 ans d'expérience, je souhaite obtenir un passeport talent pour la France. J'ai une offre d'emploi chez une startup parisienne. Budget flexible, démarrage urgent car l'entreprise attend ma réponse.",
                "lead_source": "WEBSITE"
            },
            {
                "name": "Sarah Johnson",
                "email": "sarah.j.canada@outlook.com", 
                "phone": "+1 438 123 4567",
                "country": "Canada",
                "visa_type": "Résidence Permanente (Entrée Express)",
                "budget_range": "3000-5000€",
                "urgency_level": "NORMAL",
                "message": "Professionnelle RH au Maroc, j'aimerais immigrer au Canada via Entrée Express. Score CRS estimé à 450 points. Recherche accompagnement pour optimiser mon dossier et préparer les documents.",
                "lead_source": "WEBSITE"
            },
            {
                "name": "Ahmed Benali",
                "email": "ahmed.benali.pro@yahoo.fr",
                "phone": "+212 6 87 65 43 21",
                "country": "Canada", 
                "visa_type": "Permis de Travail",
                "budget_range": "1000-3000€",
                "urgency_level": "FLEXIBLE",
                "message": "Médecin généraliste, j'envisage de travailler au Canada. Besoin d'informations sur l'équivalence de diplôme et les démarches pour obtenir un permis de travail. Processus peut prendre du temps.",
                "lead_source": "WEBSITE"
            },
            {
                "name": "Elena Rodriguez",
                "email": "elena.rodriguez.design@gmail.com",
                "phone": "+34 612 345 678",
                "country": "France",
                "visa_type": "Visa Étudiant", 
                "budget_range": "À discuter",
                "urgency_level": "URGENT",
                "message": "Designer graphique espagnole, je veux faire un master en France à l'ENSAD. Candidature déjà acceptée, besoin urgent d'aide pour le visa étudiant et logement. Rentrée en septembre.",
                "lead_source": "WEBSITE"
            },
            {
                "name": "Michael Thompson",
                "email": "mthompson.consulting@protonmail.com",
                "phone": "+44 20 7946 0958",
                "country": "Canada",
                "visa_type": "Permis d'Études",
                "budget_range": "5000+€",
                "urgency_level": "NORMAL", 
                "message": "Consultant britannique, je souhaite faire un MBA à l'Université de Toronto. Dossier académique solide, entreprise prête à financer. Recherche accompagnement premium pour maximiser les chances.",
                "lead_source": "WEBSITE"
            },
            {
                "name": "Liu Wei",
                "email": "liu.wei.tech@126.com",
                "phone": "+86 138 0013 8000",
                "country": "France",
                "visa_type": "Carte de Résident",
                "budget_range": "3000-5000€", 
                "urgency_level": "FLEXIBLE",
                "message": "Développeur senior en Chine, diplômé d'une école française. Je vis en France depuis 3 ans avec visa travail, je souhaite demander la carte de résident pour stabiliser ma situation.",
                "lead_source": "WEBSITE"
            },
            {
                "name": "Fatima Al-Zahra",
                "email": "fatima.alzahra.lawyer@hotmail.com",
                "phone": "+971 50 123 4567",
                "country": "Canada",
                "visa_type": "Parrainage Familial",
                "budget_range": "1000-3000€",
                "urgency_level": "NORMAL",
                "message": "Avocate aux Émirats, mon mari a la résidence permanente canadienne. Nous voulons lancer la procédure de parrainage familial. Dossier complexe car j'ai des enfants d'un premier mariage.",
                "lead_source": "WEBSITE"
            },
            {
                "name": "Carlos Silva",
                "email": "carlos.silva.entrepreneur@gmail.com", 
                "phone": "+55 11 99999 8888",
                "country": "France",
                "visa_type": "Permis de Travail (Passeport Talent)",
                "budget_range": "5000+€",
                "urgency_level": "URGENT",
                "message": "Entrepreneur brésilien dans la fintech, je veux créer ma startup en France. Projet innovant avec financement déjà sécurisé. Besoin urgent du passeport talent entrepreneur. Budget non limitatif.",
                "lead_source": "WEBSITE"
            },
            {
                "name": "Priya Sharma",
                "email": "priya.sharma.research@university.edu",
                "country": "Canada",
                "visa_type": "Permis d'Études", 
                "budget_range": "À discuter",
                "urgency_level": "FLEXIBLE",
                "message": "Chercheuse en biomédecine, j'ai obtenu une bourse complète pour un doctorat à McGill. Processus peut être long, je veux m'assurer de ne rien rater dans les démarches administratives.",
                "lead_source": "WEBSITE"
            },
            {
                "name": "Dimitri Volkov",
                "email": "dimitri.volkov.art@yandex.ru",
                "phone": "+7 495 123 4567", 
                "country": "France",
                "visa_type": "Visa Touristique",
                "budget_range": "1000-3000€",
                "urgency_level": "URGENT",
                "message": "Artiste russe, invité à une exposition à Paris le mois prochain. Besoin urgent d'aide pour visa Schengen, dossier artistique complexe à présenter. Première demande.",
                "lead_source": "WEBSITE"
            }
        ]
        
        return profiles

    def create_contact_messages(self):
        """Créer des messages de contact variés"""
        print("\n📝 Création des messages de contact...")
        
        profiles = self.get_sample_contact_data()
        
        for i, profile in enumerate(profiles):
            try:
                print(f"   Création contact {i+1}/10: {profile['name']}")
                
                response = self.session.post(f"{API_BASE}/contact-messages", json=profile)
                
                if response.status_code in [200, 201]:
                    message_data = response.json()
                    self.created_messages.append(message_data)
                    print(f"   ✅ Contact créé - Lead Score: {message_data.get('conversion_probability', 'N/A')}%")
                else:
                    print(f"   ❌ Erreur création contact: {response.status_code}")
                    
                # Petite pause pour ne pas surcharger
                time.sleep(0.5)
                
            except Exception as e:
                print(f"   ❌ Exception: {e}")
        
        print(f"\n✅ {len(self.created_messages)} messages de contact créés")

    def test_manager_crm_view(self):
        """Tester la vue CRM Manager"""
        print("\n🏢 Test vue CRM Manager...")
        
        if not self.manager_token:
            print("❌ Token manager requis")
            return
            
        headers = {"Authorization": f"Bearer {self.manager_token}"}
        
        # 1. Récupérer tous les messages
        print("   📋 Récupération de tous les messages...")
        response = self.session.get(f"{API_BASE}/contact-messages", headers=headers)
        if response.status_code == 200:
            all_messages = response.json()
            print(f"   ✅ {len(all_messages)} messages récupérés par Manager")
            
            # Afficher statistiques
            statuses = {}
            countries = {}
            urgency_levels = {}
            
            for msg in all_messages:
                # Compter par statut
                status = msg.get('status', 'unknown')
                statuses[status] = statuses.get(status, 0) + 1
                
                # Compter par pays
                country = msg.get('country', 'unknown')
                countries[country] = countries.get(country, 0) + 1
                
                # Compter par urgence
                urgency = msg.get('urgency_level', 'unknown')
                urgency_levels[urgency] = urgency_levels.get(urgency, 0) + 1
            
            print(f"   📊 Répartition par statut: {statuses}")
            print(f"   🌍 Répartition par pays: {countries}")
            print(f"   ⏰ Répartition par urgence: {urgency_levels}")
        
        # 2. Filtrer par statut NEW
        print("   🔍 Test filtre par statut NEW...")
        response = self.session.get(f"{API_BASE}/contact-messages?status=NEW", headers=headers)
        if response.status_code == 200:
            new_messages = response.json()
            print(f"   ✅ {len(new_messages)} messages avec statut NEW")
        
        # 3. Tester assignation d'un message à l'employé
        if self.created_messages and len(all_messages) > 0:
            print("   👥 Test assignation à un employé...")
            
            # Prendre le premier message non assigné
            unassigned_message = None
            for msg in all_messages:
                if not msg.get('assigned_to'):
                    unassigned_message = msg
                    break
            
            if unassigned_message:
                # Récupérer les employés
                employees_response = self.session.get(f"{API_BASE}/employees", headers=headers)
                if employees_response.status_code == 200:
                    employees = employees_response.json()
                    if employees:
                        employee_id = employees[0]['id']
                        
                        assign_data = {"employee_id": employee_id}
                        assign_response = self.session.patch(
                            f"{API_BASE}/contact-messages/{unassigned_message['id']}/assign", 
                            json=assign_data, 
                            headers=headers
                        )
                        
                        if assign_response.status_code == 200:
                            print(f"   ✅ Message assigné à l'employé {employees[0]['full_name']}")
                        else:
                            print(f"   ❌ Erreur assignation: {assign_response.status_code}")

    def test_employee_crm_view(self):
        """Tester la vue CRM Employé"""
        print("\n👤 Test vue CRM Employé...")
        
        if not self.employee_token:
            print("❌ Token employé requis")
            return
            
        headers = {"Authorization": f"Bearer {self.employee_token}"}
        
        # 1. Récupérer les messages assignés à l'employé
        print("   📋 Récupération messages assignés à l'employé...")
        response = self.session.get(f"{API_BASE}/contact-messages", headers=headers)
        if response.status_code == 200:
            assigned_messages = response.json()
            print(f"   ✅ {len(assigned_messages)} messages assignés à l'employé")
            
            # 2. Tester mise à jour de statut
            if assigned_messages:
                message_id = assigned_messages[0]['id']
                print(f"   📝 Test mise à jour statut pour message {message_id}")
                
                status_data = {"status": "read"}
                status_response = self.session.patch(
                    f"{API_BASE}/contact-messages/{message_id}/status", 
                    json=status_data, 
                    headers=headers
                )
                
                if status_response.status_code == 200:
                    print("   ✅ Statut mis à jour vers 'read'")
                else:
                    print(f"   ❌ Erreur mise à jour statut: {status_response.status_code}")
                
                # 3. Tester réponse à un message
                print(f"   💬 Test réponse au message {message_id}")
                
                response_data = {
                    "subject": "Re: Votre demande d'information sur l'immigration",
                    "message": "Bonjour,\n\nMerci pour votre message. Nous avons bien reçu votre demande concernant votre projet d'immigration. Un de nos experts va examiner votre profil et vous contacter sous 48h pour discuter de vos options.\n\nCordialement,\nÉquipe ALORIA AGENCY"
                }
                
                response_resp = self.session.post(
                    f"{API_BASE}/contact-messages/{message_id}/respond", 
                    json=response_data, 
                    headers=headers
                )
                
                if response_resp.status_code == 200:
                    response_result = response_resp.json()
                    print(f"   ✅ Réponse envoyée - ID: {response_result.get('response_id')}")
                else:
                    print(f"   ❌ Erreur envoi réponse: {response_resp.status_code}")
        else:
            print(f"   ❌ Erreur récupération messages: {response.status_code}")

    def test_lead_scoring_scenarios(self):
        """Tester différents scénarios de lead scoring"""
        print("\n🎯 Test scenarios de lead scoring...")
        
        # Scénarios de test avec scores attendus
        test_scenarios = [
            {
                "name": "Lead Premium - Score Maximum",
                "data": {
                    "name": "Alexandre Durand",
                    "email": "alex.durand@company.com",
                    "phone": "+33 1 23 45 67 89",
                    "country": "France",
                    "visa_type": "Permis de Travail (Passeport Talent)",
                    "budget_range": "5000+€",
                    "urgency_level": "URGENT", 
                    "message": "Directeur technique dans une multinationale, j'ai une proposition d'emploi à Paris dans une entreprise du CAC 40. Budget illimité pour l'accompagnement, démarrage immédiat requis. Profil senior avec expérience internationale, parlant parfaitement français.",
                    "lead_source": "WEBSITE"
                },
                "expected_score_min": 90
            },
            {
                "name": "Lead Moyen - Score Modéré",
                "data": {
                    "name": "Sophie Martin",
                    "email": "sophie.m@email.com", 
                    "country": "Canada",
                    "visa_type": "Permis d'Études",
                    "budget_range": "1000-3000€",
                    "urgency_level": "NORMAL",
                    "message": "Étudiante souhaitant faire un master au Canada.",
                    "lead_source": "WEBSITE"
                },
                "expected_score_min": 40,
                "expected_score_max": 70
            },
            {
                "name": "Lead Faible - Score Minimum",
                "data": {
                    "name": "Test User",
                    "email": "test@test.com",
                    "country": "Autre",
                    "message": "Information générale.",
                    "lead_source": "WEBSITE"
                },
                "expected_score_max": 60
            }
        ]
        
        for scenario in test_scenarios:
            print(f"   🧪 Test: {scenario['name']}")
            
            response = self.session.post(f"{API_BASE}/contact-messages", json=scenario['data'])
            
            if response.status_code in [200, 201]:
                result = response.json()
                score = result.get('conversion_probability', 0)
                
                print(f"   📊 Score obtenu: {score}%")
                
                # Vérifier les contraintes de score
                if 'expected_score_min' in scenario:
                    if score >= scenario['expected_score_min']:
                        print(f"   ✅ Score >= {scenario['expected_score_min']}% comme attendu")
                    else:
                        print(f"   ⚠️ Score {score}% < {scenario['expected_score_min']}% attendu")
                
                if 'expected_score_max' in scenario:
                    if score <= scenario['expected_score_max']:
                        print(f"   ✅ Score <= {scenario['expected_score_max']}% comme attendu")
                    else:
                        print(f"   ⚠️ Score {score}% > {scenario['expected_score_max']}% attendu")
            else:
                print(f"   ❌ Erreur création: {response.status_code}")

    def generate_analytics_report(self):
        """Générer un rapport analytique des données CRM"""
        print("\n📈 Génération rapport analytique...")
        
        if not self.manager_token:
            return
            
        headers = {"Authorization": f"Bearer {self.manager_token}"}
        
        # Récupérer tous les messages pour analyse
        response = self.session.get(f"{API_BASE}/contact-messages", headers=headers)
        if response.status_code != 200:
            print("❌ Impossible de récupérer les données pour le rapport")
            return
            
        messages = response.json()
        
        if not messages:
            print("📊 Aucune donnée disponible pour le rapport")
            return
        
        print(f"\n📋 RAPPORT ANALYTIQUE CRM - {len(messages)} messages analysés")
        print("="*60)
        
        # 1. Répartition par pays
        countries = {}
        for msg in messages:
            country = msg.get('country', 'Non spécifié')
            countries[country] = countries.get(country, 0) + 1
        
        print("\n🌍 RÉPARTITION PAR PAYS:")
        for country, count in sorted(countries.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(messages)) * 100
            print(f"   {country}: {count} ({percentage:.1f}%)")
        
        # 2. Répartition par type de visa
        visa_types = {}
        for msg in messages:
            visa_type = msg.get('visa_type', 'Non spécifié')
            visa_types[visa_type] = visa_types.get(visa_type, 0) + 1
        
        print("\n📄 RÉPARTITION PAR TYPE DE VISA:")
        for visa_type, count in sorted(visa_types.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(messages)) * 100
            print(f"   {visa_type}: {count} ({percentage:.1f}%)")
        
        # 3. Analyse des lead scores
        scores = [msg.get('conversion_probability', 0) for msg in messages if msg.get('conversion_probability') is not None]
        
        if scores:
            avg_score = sum(scores) / len(scores)
            min_score = min(scores)
            max_score = max(scores)
            
            high_quality_leads = len([s for s in scores if s >= 80])
            medium_quality_leads = len([s for s in scores if 50 <= s < 80])
            low_quality_leads = len([s for s in scores if s < 50])
            
            print("\n🎯 ANALYSE LEAD SCORING:")
            print(f"   Score moyen: {avg_score:.1f}%")
            print(f"   Score min/max: {min_score}% - {max_score}%")
            print(f"   Leads haute qualité (≥80%): {high_quality_leads} ({(high_quality_leads/len(scores)*100):.1f}%)")
            print(f"   Leads qualité moyenne (50-79%): {medium_quality_leads} ({(medium_quality_leads/len(scores)*100):.1f}%)")
            print(f"   Leads qualité faible (<50%): {low_quality_leads} ({(low_quality_leads/len(scores)*100):.1f}%)")
        
        # 4. Répartition par budget
        budgets = {}
        for msg in messages:
            budget = msg.get('budget_range', 'Non spécifié')
            budgets[budget] = budgets.get(budget, 0) + 1
        
        print("\n💰 RÉPARTITION PAR BUDGET:")
        for budget, count in sorted(budgets.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(messages)) * 100
            print(f"   {budget}: {count} ({percentage:.1f}%)")
        
        # 5. Répartition par urgence
        urgency_levels = {}
        for msg in messages:
            urgency = msg.get('urgency_level', 'Non spécifié')
            urgency_levels[urgency] = urgency_levels.get(urgency, 0) + 1
        
        print("\n⏰ RÉPARTITION PAR URGENCE:")
        for urgency, count in sorted(urgency_levels.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(messages)) * 100
            print(f"   {urgency}: {count} ({percentage:.1f}%)")
        
        # 6. Statuts des messages
        statuses = {}
        for msg in messages:
            status = msg.get('status', 'Non spécifié')
            statuses[status] = statuses.get(status, 0) + 1
        
        print("\n📊 RÉPARTITION PAR STATUT:")
        for status, count in sorted(statuses.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(messages)) * 100
            print(f"   {status}: {count} ({percentage:.1f}%)")
        
        print("\n" + "="*60)
        print("✅ Rapport analytique généré avec succès")

    def run_complete_test(self):
        """Exécuter la suite complète de tests"""
        print("🚀 DÉBUT DES TESTS CRM COMPLETS")
        print("="*50)
        
        # 1. Connexions
        if not self.login_manager():
            print("❌ Impossible de continuer sans connexion Manager")
            return
            
        if not self.create_employee_for_testing():
            print("⚠️ Continuation sans employé de test")
        
        # 2. Création des données de test
        self.create_contact_messages()
        
        # 3. Tests des vues
        self.test_manager_crm_view()
        self.test_employee_crm_view()
        
        # 4. Tests lead scoring
        self.test_lead_scoring_scenarios()
        
        # 5. Rapport analytique
        self.generate_analytics_report()
        
        print("\n🎉 TESTS CRM TERMINÉS AVEC SUCCÈS!")
        print(f"📊 {len(self.created_messages)} messages de contact créés")
        print("✅ Toutes les fonctionnalités CRM testées")

if __name__ == "__main__":
    print("ALORIA AGENCY - Générateur de données CRM")
    print("Création de données de test réalistes pour le système CRM")
    print("-" * 60)
    
    generator = CRMDataGenerator()
    generator.run_complete_test()