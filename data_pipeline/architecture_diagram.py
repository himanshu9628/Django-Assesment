#!/usr/bin/env python3
"""
Data Pipeline Architecture Diagram Generator
This script creates a visual representation of the event-driven data pipeline architecture.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

def create_architecture_diagram():
    """Create a comprehensive architecture diagram for the data pipeline."""
    
    # Create figure and axis
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # Colors
    colors = {
        'ingestion': '#FF6B6B',
        'lightweight': '#4ECDC4',
        'heavy': '#45B7D1',
        'storage': '#96CEB4',
        'monitoring': '#FFEAA7'
    }
    
    # Define components with positions
    components = {
        # Event Ingestion Layer
        'API Gateway': {'pos': (1, 10), 'color': colors['ingestion'], 'size': (1.5, 0.8)},
        'Load Balancer': {'pos': (3, 10), 'color': colors['ingestion'], 'size': (1.5, 0.8)},
        'Kafka': {'pos': (5, 10), 'color': colors['ingestion'], 'size': (1.5, 0.8)},
        'Kafka Connect': {'pos': (7, 10), 'color': colors['ingestion'], 'size': (1.5, 0.8)},
        
        # Lightweight Processing Layer
        'Kafka Streams': {'pos': (2, 8), 'color': colors['lightweight'], 'size': (1.5, 0.8)},
        'Redis Cache': {'pos': (4, 8), 'color': colors['lightweight'], 'size': (1.5, 0.8)},
        'Event Validation': {'pos': (6, 8), 'color': colors['lightweight'], 'size': (1.5, 0.8)},
        
        # Heavy Processing Layer
        'Apache Spark': {'pos': (2, 6), 'color': colors['heavy'], 'size': (1.5, 0.8)},
        'Celery Workers': {'pos': (4, 6), 'color': colors['heavy'], 'size': (1.5, 0.8)},
        'Dead Letter Queue': {'pos': (6, 6), 'color': colors['heavy'], 'size': (1.5, 0.8)},
        
        # Data Storage Layer
        'Data Lake': {'pos': (1, 4), 'color': colors['storage'], 'size': (1.5, 0.8)},
        'Data Warehouse': {'pos': (3, 4), 'color': colors['storage'], 'size': (1.5, 0.8)},
        'Analytics DB': {'pos': (5, 4), 'color': colors['storage'], 'size': (1.5, 0.8)},
        'Metadata Store': {'pos': (7, 4), 'color': colors['storage'], 'size': (1.5, 0.8)},
        
        # Monitoring Layer
        'Prometheus': {'pos': (1, 2), 'color': colors['monitoring'], 'size': (1.5, 0.8)},
        'Grafana': {'pos': (3, 2), 'color': colors['monitoring'], 'size': (1.5, 0.8)},
        'Jaeger': {'pos': (5, 2), 'color': colors['monitoring'], 'size': (1.5, 0.8)},
        'ELK Stack': {'pos': (7, 2), 'color': colors['monitoring'], 'size': (1.5, 0.8)},
    }
    
    # Draw components
    for name, config in components.items():
        x, y = config['pos']
        width, height = config['size']
        color = config['color']
        
        # Create rounded rectangle
        box = FancyBboxPatch(
            (x - width/2, y - height/2), width, height,
            boxstyle="round,pad=0.1",
            facecolor=color,
            edgecolor='black',
            linewidth=1
        )
        ax.add_patch(box)
        
        # Add text
        ax.text(x, y, name, ha='center', va='center', fontsize=8, fontweight='bold')
    
    # Add layer labels
    layer_labels = [
        ('Event Ingestion Layer', 5, 11.5),
        ('Lightweight Processing Layer', 5, 9.5),
        ('Heavy Processing Layer', 5, 7.5),
        ('Data Storage Layer', 5, 5.5),
        ('Monitoring & Observability', 5, 3.5)
    ]
    
    for label, x, y in layer_labels:
        ax.text(x, y, label, ha='center', va='center', fontsize=12, fontweight='bold')
    
    # Add data flow arrows
    arrows = [
        # Ingestion flow
        ((1, 9.6), (3, 9.6)),  # API Gateway to Load Balancer
        ((3, 9.6), (5, 9.6)),  # Load Balancer to Kafka
        ((5, 9.6), (7, 9.6)),  # Kafka to Kafka Connect
        
        # Processing flow
        ((5, 9.2), (2, 8.4)),  # Kafka to Kafka Streams
        ((2, 7.6), (4, 7.6)),  # Kafka Streams to Redis
        ((4, 7.6), (6, 7.6)),  # Redis to Event Validation
        ((6, 7.6), (2, 6.4)),  # Event Validation to Spark
        ((2, 5.6), (4, 5.6)),  # Spark to Celery
        ((4, 5.6), (6, 5.6)),  # Celery to Dead Letter Queue
        
        # Storage flow
        ((2, 5.2), (1, 4.4)),  # Spark to Data Lake
        ((4, 5.2), (3, 4.4)),  # Celery to Data Warehouse
        ((6, 5.2), (5, 4.4)),  # Dead Letter Queue to Analytics DB
        
        # Monitoring connections
        ((1, 3.6), (1, 2.4)),  # Data Lake to Prometheus
        ((3, 3.6), (3, 2.4)),  # Data Warehouse to Grafana
        ((5, 3.6), (5, 2.4)),  # Analytics DB to Jaeger
        ((7, 3.6), (7, 2.4)),  # Metadata Store to ELK
    ]
    
    for start, end in arrows:
        arrow = ConnectionPatch(
            start, end, "data", "data",
            arrowstyle="->", shrinkA=5, shrinkB=5,
            mutation_scale=20, fc="black", linewidth=1.5
        )
        ax.add_patch(arrow)
    
    # Add title
    ax.text(5, 11.8, 'Event-Driven Data Pipeline Architecture', 
            ha='center', va='center', fontsize=16, fontweight='bold')
    
    # Add legend
    legend_elements = [
        patches.Patch(color=colors['ingestion'], label='Event Ingestion'),
        patches.Patch(color=colors['lightweight'], label='Lightweight Processing'),
        patches.Patch(color=colors['heavy'], label='Heavy Processing'),
        patches.Patch(color=colors['storage'], label='Data Storage'),
        patches.Patch(color=colors['monitoring'], label='Monitoring')
    ]
    
    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.98))
    
    plt.tight_layout()
    return fig

def create_data_flow_diagram():
    """Create a detailed data flow diagram."""
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Define flow stages
    stages = [
        ('Event Sources', 1, 4, '#FF6B6B'),
        ('API Gateway', 3, 4, '#4ECDC4'),
        ('Kafka', 5, 4, '#45B7D1'),
        ('Kafka Streams', 7, 4, '#96CEB4'),
        ('Spark', 9, 4, '#FFEAA7'),
        ('Data Warehouse', 11, 4, '#DDA0DD')
    ]
    
    # Draw stages
    for name, x, y, color in stages:
        box = FancyBboxPatch(
            (x - 0.8, y - 0.4), 1.6, 0.8,
            boxstyle="round,pad=0.05",
            facecolor=color,
            edgecolor='black',
            linewidth=1
        )
        ax.add_patch(box)
        ax.text(x, y, name, ha='center', va='center', fontsize=9, fontweight='bold')
    
    # Add flow arrows
    for i in range(len(stages) - 1):
        start_x = stages[i][1] + 0.8
        end_x = stages[i + 1][1] - 0.8
        y = stages[i][2]
        
        arrow = ConnectionPatch(
            (start_x, y), (end_x, y), "data", "data",
            arrowstyle="->", shrinkA=5, shrinkB=5,
            mutation_scale=15, fc="black", linewidth=2
        )
        ax.add_patch(arrow)
    
    # Add processing details
    details = [
        ('Rate Limiting', 3, 2.5),
        ('Validation', 5, 2.5),
        ('Enrichment', 7, 2.5),
        ('Transformation', 9, 2.5),
        ('Batch Load', 11, 2.5)
    ]
    
    for detail, x, y in details:
        ax.text(x, y, detail, ha='center', va='center', fontsize=8, style='italic')
    
    # Add title
    ax.text(6, 7.5, 'Data Flow Pipeline', 
            ha='center', va='center', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    return fig

if __name__ == "__main__":
    # Create architecture diagram
    arch_fig = create_architecture_diagram()
    arch_fig.savefig('data_pipeline/architecture_diagram.png', dpi=300, bbox_inches='tight')
    
    # Create data flow diagram
    flow_fig = create_data_flow_diagram()
    flow_fig.savefig('data_pipeline/data_flow_diagram.png', dpi=300, bbox_inches='tight')
    
    print("Architecture diagrams generated successfully!")
    print("Files saved as:")
    print("- data_pipeline/architecture_diagram.png")
    print("- data_pipeline/data_flow_diagram.png") 