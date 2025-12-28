from nexus import create_app
from extensions import db
from models.subject_model import Subject

app = create_app()

# Extensive mapping of subject keywords to unique Unsplash images
# Added more specific mappings for UHV, workshop, manufacturing, and others.
image_pool = {
    'universal human values': ['https://images.unsplash.com/photo-1521791136064-7986c29596ad?q=80&w=2070'], # handshake/peace
    'workshop': ['https://images.unsplash.com/photo-1504917595217-d4dc5f612b60?q=80&w=2070'], # tools
    'manufacturing': ['https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?q=80&w=2070'], # factory/industrial
    'mathematics': [
        'https://images.unsplash.com/photo-1509228468518-180dd48a5791?q=80&w=2070',
        'https://images.unsplash.com/photo-1635070041078-e363dbe005cb?q=80&w=2070',
        'https://images.unsplash.com/photo-1632571401005-458e9d244591?q=80&w=2071'
    ],
    'physics': [
        'https://images.unsplash.com/photo-1636466497217-26a8cbeaf0aa?q=80&w=2070',
        'https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2072',
        'https://images.unsplash.com/photo-1532094349884-543bb1198c33?q=80&w=2070'
    ],
    'electronics': [
        'https://images.unsplash.com/photo-1517077304055-6e89abbf09b0?q=80&w=2069',
        'https://images.unsplash.com/photo-1555664424-778a1e5e1b48?q=80&w=2070'
    ],
    'programming': [
        'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?q=80&w=2070',
        'https://images.unsplash.com/photo-1587620962725-abab7fe55159?q=80&w=2031',
        'https://images.unsplash.com/photo-1542831371-29b0f74f9713?q=80&w=2070'
    ],
    'data structures': ['https://images.unsplash.com/photo-1516116216624-53e697fedbea?q=80&w=2128'],
    'algorithms': ['https://images.unsplash.com/photo-1504639725590-34d0984388bd?q=80&w=1974'],
    'operating system': ['https://images.unsplash.com/photo-1629654297299-c8506221ca97?q=80&w=1974'],
    'database': ['https://images.unsplash.com/photo-1544383835-bda2bc66a55d?q=80&w=2021'],
    'networks': ['https://images.unsplash.com/photo-1544197150-b99a580bb7a8?q=80&w=2070'],
    'web tech': ['https://images.unsplash.com/photo-1547658719-da2b51169166?q=80&w=2064'],
    'artificial intelligence': ['https://images.unsplash.com/photo-1677442136019-21780ecad995?q=80&w=2070'],
    'cyber security': ['https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=2070'],
    'english': ['https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?q=80&w=2073'],
    'chemistry': ['https://images.unsplash.com/photo-1532187863486-abf51ad446fe?q=80&w=2070'],
    'management': ['https://images.unsplash.com/photo-1454165833767-02acd052c0e6?q=80&w=2070'],
    'biology': ['https://images.unsplash.com/photo-1530026405186-ed1f139313f8?q=80&w=2070'],
    'sports': ['https://images.unsplash.com/photo-1461896836934-ffe607ba8211?q=80&w=2070'],
    'graphics': ['https://images.unsplash.com/photo-1558655146-d09347e92766?q=80&w=2064'],
    'design thinking': ['https://images.unsplash.com/photo-1586717791821-3f44a563eb4c?q=80&w=2070'],
    'constitution': ['https://images.unsplash.com/photo-1589829545856-d10d557cf95f?q=80&w=2070'],
    'environmental': ['https://images.unsplash.com/photo-1473081556163-2a17281fe7df?q=80&w=1974'],
    'microprocessor': ['https://images.unsplash.com/photo-1591799244391-912981ac9a11?q=80&w=2070'],
    'discrete': ['https://images.unsplash.com/photo-1509228468518-180dd48a5791?q=80&w=2070'],
}

default_images = [
    'https://images.unsplash.com/photo-1515879218367-8466d910aaa4?q=80&w=2069',
    'https://images.unsplash.com/photo-1550439062-609e1531270e?q=80&w=2070',
    'https://images.unsplash.com/photo-1510511459019-5dee2c14fd8c?q=80&w=2070'
]

used_images = set()

def get_unique_image(title):
    global used_images
    title_lower = title.lower()
    
    # Check for specific keyword matches
    for keyword, urls in image_pool.items():
        if keyword in title_lower:
            for url in urls:
                if url not in used_images:
                    used_images.add(url)
                    return url
    
    # Try general defaults if no keyword match or all matches used
    for url in default_images:
        if url not in used_images:
            used_images.add(url)
            return url
            
    # If we run out of unique images, just use a random one from the pool
    import random
    all_urls = [url for sublist in image_pool.values() for url in sublist] + default_images
    return random.choice(all_urls)

with app.app_context():
    subjects = Subject.query.all()
    print(f"Total subjects to update: {len(subjects)}")
    
    # Reset used images set to allow re-assignment if we're running it again
    used_images = set()
    
    for sub in subjects:
        sub.image_url = get_unique_image(sub.title)
        print(f"Updated {sub.title} -> {sub.image_url}")
        
    db.session.commit()
    print("All subject backgrounds updated with unique and refined images.")
