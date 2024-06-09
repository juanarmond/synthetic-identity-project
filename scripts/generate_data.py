import networkx as nx
import pandas as pd
import random
import uuid
import pickle
import pycountry
from faker import Faker
from difflib import SequenceMatcher

class IdentityIslandGenerator:
    def __init__(self):
        self.G = nx.DiGraph()
        self.fake = Faker()
        self.country_locale_map = self._create_country_locale_map()
        self.identity_islands = []

    def _create_country_locale_map(self):
        return {
            'AL': 'sq_AL', 'AM': 'hy_AM', 'AR': 'es_AR', 'AT': 'de_AT', 'AZ': 'az_AZ', 'BE': 'fr_BE',
            'BG': 'bg_BG', 'BN': 'bn_BD', 'BO': 'es', 'BR': 'pt_BR', 'CA': 'fr_CA', 'CH': 'de_CH',
            'CL': 'es_CL', 'CN': 'zh_CN', 'CO': 'es_CO', 'CR': 'es', 'CS': 'cs_CZ', 'CU': 'es',
            'DE': 'de', 'DO': 'es', 'EC': 'es', 'EE': 'et_EE', 'ES': 'es_ES', 'FI': 'fi_FI', 'FR': 'fr_FR',
            'GB': 'en_GB', 'GE': 'ka_GE', 'GR': 'el_GR', 'GT': 'es', 'HN': 'es', 'HR': 'hr_HR', 'HU': 'hu_HU',
            'ID': 'id_ID', 'IE': 'en_IE', 'IL': 'he_IL', 'IN': 'en_IN', 'IR': 'fa_IR', 'IT': 'it_IT',
            'JP': 'ja_JP', 'KR': 'ko_KR', 'MX': 'es_MX', 'NI': 'es', 'NL': 'nl_NL', 'NO': 'no_NO',
            'NZ': 'en_NZ', 'PA': 'es', 'PE': 'es', 'PL': 'pl_PL', 'PT': 'pt_PT', 'PY': 'es', 'RO': 'ro_RO',
            'RU': 'ru_RU', 'SA': 'ar_SA', 'SE': 'sv_SE', 'SI': 'sl_SI', 'SK': 'sk_SK', 'SV': 'es',
            'TH': 'th_TH', 'TR': 'tr_TR', 'TW': 'zh_TW', 'UA': 'uk_UA', 'UY': 'es', 'VE': 'es', 'ZA': 'zu_ZA'
        }

    def create_identity_island(self, locale_fake, base_name, date_of_birth, nationality, num_identities):
        base_identity = {
            'id': str(uuid.uuid4()),
            'type': 'Identity',
            'name': base_name,
            'age': (pd.to_datetime('today') - pd.to_datetime(date_of_birth, dayfirst=True)).days // 365,
            'date_of_birth': date_of_birth,
            'nationality': nationality
        }
        self.G.add_node(base_identity['id'], **base_identity)

        second_name = locale_fake.first_name()
        middle_name = locale_fake.last_name()
        
        partial_names = [
            f"{base_name.split()[0]} {base_name.split()[-1]}",
            f"{base_name.split()[0]} {second_name} {base_name.split()[-1]}",
            f"{base_name.split()[0]} {second_name} {middle_name} {base_name.split()[-1]}",
            f"{base_name.split()[0]} {middle_name} {base_name.split()[-1]}"
        ]
        
        identities = [base_identity['id']]
        for partial_name in random.sample(partial_names, min(num_identities, len(partial_names))):
            identity = {
                'id': str(uuid.uuid4()),
                'type': 'Identity',
                'name': partial_name,
                'age': base_identity['age'],
                'date_of_birth': date_of_birth,
                'nationality': nationality
            }
            self.G.add_node(identity['id'], **identity)
            self.G.add_edge(base_identity['id'], identity['id'], type='IDENTITY_EQUIVALENCE')
            identities.append(identity['id'])
        
        return identities

    def generate_random_identity_island(self):
        country_code = self.fake.country_code()
        locale = self.country_locale_map.get(country_code, 'en_US')
        locale_fake = Faker(locale)
        base_name = f"{locale_fake.first_name()} {locale_fake.last_name()}"
        date_of_birth = self.fake.date_of_birth(minimum_age=1, maximum_age=80).strftime('%d/%m/%Y')
        nationality = pycountry.countries.get(alpha_2=country_code).alpha_3
        return self.create_identity_island(locale_fake, base_name, date_of_birth, nationality, random.randint(1, 5))

    def add_edges_within_island(self, island):
        reference_nodes = [{'id': str(uuid.uuid4()), 'type': 'Reference', 'doc_type': random.choice(['PASSPORT', 'NATURALISATION', 'VISA_1', 'VISA_2', 'NATIONAL_IDENTITY_CARD']), 'doc_number': self.fake.ssn()} for _ in range(5)]
        event_nodes = [{'id': str(uuid.uuid4()), 'type': 'Event', 'event_type': 'BIOMETRIC_VERIFICATION', 'event_date': self.fake.date()} for _ in range(2)]
        
        for node in reference_nodes + event_nodes:
            self.G.add_node(node['id'], **node)
        
        for identity in island:
            if random.random() < 0.5:
                target = random.choice(island)
                self.G.add_edge(identity, target, type='INCLUDED_IN')

            if random.random() < 0.5:
                target = random.choice(reference_nodes)['id']
                self.G.add_edge(identity, target, type='CITED_BY')

            if random.random() < 0.5:
                target = random.choice(reference_nodes)['id']
                self.G.add_edge(identity, target, type='IDENTIFIED_THROUGH_BIOMETRICS')

            if random.random() < 0.5:
                target = random.choice(island)
                self.G.add_edge(identity, target, type='IDENTITY_EQUIVALENCE')

            if random.random() < 0.5:
                target = random.choice(island)
                self.G.add_edge(identity, target, type='MANUAL_IDENTITY_OVERRIDE')

            if random.random() < 0.5:
                target = random.choice(event_nodes)['id']
                self.G.add_edge(identity, target, type='IMMIGRATION_STATUS_LINKED')

            if random.random() < 0.5:
                target = random.choice(island)
                self.G.add_edge(identity, target, type='SAME_APPLICATION')

    def similar(self, a, b):
        return SequenceMatcher(None, a, b).ratio()

    def find_similar_identity(self, island, target_identity, attribute, threshold=0.6):
        similar_identity = None
        highest_similarity = 0

        for identity in island:
            if attribute == 'name':
                name_similarity = self.similar(target_identity['name'], identity['name'])
                if name_similarity >= threshold:
                    if target_identity['date_of_birth'] == identity['date_of_birth'] or target_identity['nationality'] == identity['nationality']:
                        if name_similarity > highest_similarity:
                            highest_similarity = name_similarity
                            similar_identity = identity['id']
            elif attribute == 'date_of_birth':
                if target_identity['date_of_birth'] == identity['date_of_birth']:
                    if target_identity['nationality'] == identity['nationality']:
                        similar_identity = identity['id']
                        break
            elif attribute == 'nationality':
                if target_identity['nationality'] == identity['nationality']:
                    if target_identity['date_of_birth'] == identity['date_of_birth']:
                        similar_identity = identity['id']
                        break

        return similar_identity

    def add_anomalies(self, anomaly_percentage):
        total_islands = len(self.identity_islands)
        num_anomalous_islands = int(total_islands * (anomaly_percentage / 100))

        for _ in range(num_anomalous_islands):
            island = random.choice(self.identity_islands)
            source_identity_id = random.choice(island)
            source_identity = self.G.nodes[source_identity_id]
            anomaly_type = random.choice(['duplicate_identity', 'inconsistent_reference', 'mislinked_identity', 'incorrect_event'])
            
            if anomaly_type == 'duplicate_identity':
                base_identity = self.G.nodes[source_identity_id]
                duplicate_identity = base_identity.copy()
                duplicate_identity['id'] = str(uuid.uuid4())
                duplicate_identity['name'] = self.fake.first_name() + " " + base_identity['name'].split()[1]
                self.G.add_node(duplicate_identity['id'], **duplicate_identity)
                self.G.add_edge(source_identity_id, duplicate_identity['id'], type='IDENTITY_EQUIVALENCE')
                island.append(duplicate_identity['id'])
                # print(f"Added duplicate identity anomaly: {duplicate_identity['name']}")

            elif anomaly_type == 'inconsistent_reference':
                inconsistent_reference = {
                    'id': str(uuid.uuid4()),
                    'type': 'Reference',
                    'doc_type': random.choice(['PASSPORT', 'NATURALISATION', 'VISA_1', 'VISA_2', 'NATIONAL_IDENTITY_CARD']),
                    'doc_number': self.fake.ssn()
                }
                self.G.add_node(inconsistent_reference['id'], **inconsistent_reference)
                target_identity_id = random.choice(island)
                self.G.add_edge(target_identity_id, inconsistent_reference['id'], type='CITED_BY')
                # print(f"Added inconsistent reference anomaly: {inconsistent_reference['doc_type']}")

            elif anomaly_type == 'mislinked_identity':
                attribute = 'name'
                unrelated_identity_island = random.choice([i for i in self.identity_islands if i != island])
                similar_identity_id = self.find_similar_identity([self.G.nodes[id] for id in unrelated_identity_island], source_identity, attribute)
                
                if similar_identity_id:
                    self.G.add_edge(source_identity_id, similar_identity_id, type='IDENTITY_EQUIVALENCE')
                    print(f"Added mislinked identity anomaly between {source_identity_id} and {similar_identity_id}")
                else:
                    unrelated_identity = random.choice([id for i in self.identity_islands for id in i if i != island])
                    self.G.add_edge(source_identity_id, unrelated_identity, type='IDENTITY_EQUIVALENCE')
                    # print(f"Added completely different identity anomaly between {source_identity_id} and {unrelated_identity}")

            elif anomaly_type == 'incorrect_event':
                incorrect_event = {
                    'id': str(uuid.uuid4()),
                    'type': 'Event',
                    'event_type': 'BIOMETRIC_VERIFICATION',
                    'event_date': self.fake.date()
                }
                self.G.add_node(incorrect_event['id'], **incorrect_event)
                target_identity_id = random.choice(island)
                self.G.add_edge(target_identity_id, incorrect_event['id'], type='IMMIGRATION_STATUS_LINKED')
                # print(f"Added incorrect event anomaly: {incorrect_event['event_type']}")

    def generate_identity_islands(self, num_islands):
        for _ in range(num_islands):
            island = self.generate_random_identity_island()
            self.identity_islands.append(island)

        for island in self.identity_islands:
            self.add_edges_within_island(island)

    def save_graph(self, filepath):
        with open(filepath, 'wb') as f:
            pickle.dump(self.G, f, pickle.HIGHEST_PROTOCOL)

    def save_identity_islands(self, filepath):
        with open(filepath, 'wb') as f:
            pickle.dump(self.identity_islands, f, pickle.HIGHEST_PROTOCOL)

    def load_graph(self, filepath):
        with open(filepath, 'rb') as f:
            self.G = pickle.load(f)

    def load_identity_islands(self, filepath):
        with open(filepath, 'rb') as f:
            self.identity_islands = pickle.load(f)

    def print_identity_islands(self):
        for i, island in enumerate(self.identity_islands, start=1):
            print(f"Identity Island {i}:")
            for identity in island:
                node_data = self.G.nodes[identity]
                print(f"  ID: {identity}, Name: {node_data['name']}, DOB: {node_data['date_of_birth']}, Nationality: {node_data['nationality']}")
            print()

    def print_identity_details(self, node_id):
        node_details = self.G.nodes[node_id]
        print(f"Node ID: {node_id}")
        print("Node Details:")
        print(node_details)
        
        print("\nIncoming Edges:")
        for u, v, data in self.G.in_edges(node_id, data=True):
            print(f"{u} -> {v} (Type: {data['type']})")
        
        print("\nOutgoing Edges:")
        for u, v, data in self.G.out_edges(node_id, data=True):
            print(f"{u} -> {v} (Type: {data['type']})")

    def debug_print_first_node(self):
        for node, attrs in self.G.nodes(data=True):
            print(f"Node ID: {node}")
            print("Attributes:")
            for attr_key, attr_value in attrs.items():
                print(f"{attr_key}: {attr_value}")
            print()
            break

    def debug_print_first_edge(self):
        for edge in self.G.edges(data=True):
            print(f"Edge from {edge[0]} to {edge[1]}")
            print("Attributes:")
            for attr_key, attr_value in edge[2].items():
                print(f"{attr_key}: {attr_value}")
            break

if __name__ == "__main__":
    generator = IdentityIslandGenerator()
    generator.generate_identity_islands(num_islands=10)
    
    # Save the graph before adding anomalies
    generator.save_graph('./data/synthetic_data/synthetic_identity_islands.gpickle')
    generator.save_identity_islands('./data/synthetic_data/identity_islands.pkl')

    # Debug prints
    print("Synthetic data generation complete.")
    print(f"Number of nodes in the graph: {generator.G.number_of_nodes()}")
    print(f"Number of edges in the graph: {generator.G.number_of_edges()}")
    # generator.debug_print_first_node()
    # generator.debug_print_first_edge()
    # generator.print_identity_islands()
    
    # Add anomalies
    generator.add_anomalies(anomaly_percentage=50)
    
    # Save the graph after adding anomalies
    generator.save_graph('./data/anomalies_data/synthetic_identity_islands.gpickle')
    generator.save_identity_islands('./data/anomalies_data/identity_islands.pkl')

    # Debug prints
    print("Synthetic data generation with anomalies complete.")
    print(f"Number of nodes in the graph: {generator.G.number_of_nodes()}")
    print(f"Number of edges in the graph: {generator.G.number_of_edges()}")
    # generator.debug_print_first_node()
    # generator.debug_print_first_edge()
    # generator.print_identity_islands()