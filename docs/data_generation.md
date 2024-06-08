# Synthetic Data Generation

## Overview

The synthetic data generation process is designed to create identity islands, which are clusters of identities representing variations of a central identity. These islands simulate real-world scenarios where individuals may have multiple forms of identification or slightly different records in different databases. The `IdentityIslandGenerator` class facilitates this process by generating realistic identity data and their interconnections.

## IdentityIslandGenerator Class

### Initialization

The `IdentityIslandGenerator` class initializes with a directed graph (`DiGraph`) from the NetworkX library to represent identity islands and their relationships. It uses the `Faker` library to generate random identity data. Additionally, it creates a mapping of country codes to locale settings to ensure that names and other attributes are generated in a culturally appropriate manner.

### Country Locale Mapping

A private method `_create_country_locale_map()` generates a dictionary that maps country codes to their respective Faker locale settings. This helps in generating localized names and other attributes that match the specified locale.

### Creating Identity Islands

1. **Base Identity**: The `create_identity_island()` method begins by creating a base identity with key attributes such as a unique ID, name, date of birth, age, and nationality. This base identity serves as the root of the identity island.

2. **Name Variations**: The method generates partial names by manipulating the base name (e.g., adding a middle name, using a second name). These variations help simulate real-world scenarios where a person might have different versions of their name.

3. **Adding Nodes and Edges**: Each identity variation is assigned a unique ID and added to the graph. The method also creates `IDENTITY_EQUIVALENCE` edges to represent the relationships between the base identity and its variations.

### Generating Random Identity Islands

The `generate_random_identity_island()` method automates the creation of identity islands by selecting a random country code and locale. It then generates a base name, date of birth, and nationality, calling `create_identity_island()` to build the island. This method ensures diversity in the generated data by using different locales and attributes.

### Adding Relationships Within Islands

To add realism, the `add_edges_within_island()` method introduces various types of edges within an identity island. These include:
- **References**: Nodes representing documents like passports or national IDs.
- **Events**: Nodes representing events such as biometric verifications.
- **Relationships**: Edges representing different types of connections, such as `INCLUDED_IN`, `CITED_BY`, `IDENTIFIED_THROUGH_BIOMETRICS`, `SAME_APPLICATION`, etc.

### Introducing Anomalies

To simulate real-world data issues, the `add_anomalies()` method introduces anomalies into the identity islands. The types of anomalies include:
- **Duplicate Identities**: Creating a duplicate identity with minor changes.
- **Inconsistent References**: Adding a reference document that doesn't logically match any identity in the island.
- **Mislinked Identities**: Linking an identity from a different island based on a similar attribute.
- **Incorrect Events**: Introducing an event that does not logically connect to the identities within the island.

### Generating and Saving Data

The `generate_identity_islands()` method generates a specified number of identity islands and adds relationships within each island. The `save_graph()` and `save_identity_islands()` methods save the generated graph and identity islands to specified file paths for further use.

### Example Usage

Here's a high-level outline of how to use the `IdentityIslandGenerator` class:

1. **Initialize the Generator**: Create an instance of the `IdentityIslandGenerator`.
2. **Generate Identity Islands**: Use the `generate_identity_islands()` method to create identity islands.
3. **Save Data**: Save the generated graph and identity islands using `save_graph()` and `save_identity_islands()`.
4. **Introduce Anomalies**: Add anomalies to the identity islands using the `add_anomalies()` method.
5. **Save Anomalous Data**: Save the graph and identity islands with anomalies.

### Debugging and Validation

The class provides various methods to assist in debugging and validation:
- **print_identity_islands()**: Prints details of all identity islands.
- **print_identity_details(node_id)**: Prints details of a specific identity node.
- **debug_print_first_node()** and **debug_print_first_edge()**: Print details of the first node and edge in the graph for quick debugging.

### Conclusion

The `IdentityIslandGenerator` class is a comprehensive tool for generating synthetic identity data, introducing anomalies, and creating complex relationships within identity islands. It provides a robust framework for testing and development in scenarios involving identity management and anomaly detection.