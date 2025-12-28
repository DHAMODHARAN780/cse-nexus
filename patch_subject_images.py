from nexus import create_app
from extensions import db
from models.subject_model import Subject

app = create_app()

def patch_images():
    with app.app_context():
        subjects = Subject.query.all()
        
        mapping = {
            'programming.png': ['python', 'java', 'programming', 'web', 'data structures', 'algorithms', 'web technology', 'javascript', 'compiler design'],
            'mathematics.png': ['mathematics', 'discrete', 'probability', 'calculus', 'physics', 'chemistry', 'biology', 'equations'],
            'ai_data.png': ['artificial intelligence', 'machine learning', 'database', 'data mining', 'big data', 'intelligence'],
            'hardware.png': ['hardware', 'microprocessor', 'digital', 'architecture', 'electronics', 'iot'],
            'networking.png': ['networks', 'cyber security', 'cloud', 'distributed', 'security']
        }
        
        updated = 0
        for s in subjects:
            title_lower = s.title.lower()
            code_lower = s.code.lower()
            
            assigned = False
            for img, keywords in mapping.items():
                if any(kw in title_lower or kw in code_lower for kw in keywords):
                    s.image_url = f'images/subjects/{img}'
                    assigned = True
                    break
            
            if not assigned:
                # Default to programming if no specific match
                s.image_url = 'images/subjects/programming.png'
            
            updated += 1
        
        db.session.commit()
        print(f"Updated {updated} subjects with background images.")

if __name__ == '__main__':
    patch_images()
