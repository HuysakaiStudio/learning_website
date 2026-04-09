# Roadmap Visualization

## Timeline Overview

```mermaid
gantt
    title Roadmap Phát triển Hệ thống Học tập
    dateFormat YYYY-MM-DD
    section Phase 1 - Core
    Flashcard UI/UX Improvements :p1-1, 2026-04-08, 14d
    Leaderboard System :p1-2, 2026-04-15, 14d
    Notification System :p1-3, after p1-2, 10d
    
    section Phase 2 - Social
    Study Groups :p2-1, 2026-05-20, 14d
    User Following :p2-2, after p2-1, 10d
    Activity Feed :p2-3, after p2-2, 7d
    
    section Phase 3 - AI
    Recommendations :p3-1, 2026-07-01, 21d
    AI Assistant :p3-2, after p3-1, 30d
    Auto-gen Flashcards :p3-3, after p3-2, 14d
    
    section Phase 4 - Mobile
    PWA Implementation :p4-1, 2026-06-01, 14d
    Performance Optimization :p4-2, after p4-1, 14d
```

## System Architecture

```mermaid
graph TB
    subgraph Client
        A[Web Browser]
        B[PWA]
    end
    
    subgraph Django Backend
        C[Views/APIs]
        D[Models]
        E[Business Logic]
    end
    
    subgraph Background
        F[Celery Workers]
        G[Celery Beat]
    end
    
    subgraph Data Layer
        H[(PostgreSQL)]
        I[(Redis Cache)]
    end
    
    subgraph External
        J[OpenAI API]
        K[Email Service]
    end
    
    A --> C
    B --> C
    C --> D
    C --> E
    E --> D
    D --> H
    C --> I
    E --> F
    G --> F
    F --> H
    F --> I
    E --> J
    F --> K
```

## Feature Dependencies

```mermaid
graph LR
    A[Flashcard UI/UX] --> B[Keyboard Shortcuts]
    A --> C[Animations]
    
    D[Leaderboard] --> E[Competitions]
    D --> F[Rank Badges]
    
    G[Notifications] --> H[Real-time Updates]
    G --> I[Email Digest]
    
    J[Study Groups] --> K[Group Chat]
    J --> L[Group Challenges]
    
    M[User Following] --> N[Activity Feed]
    N --> O[Social Engagement]
    
    P[AI Recommendations] --> Q[Personalized Learning]
    R[AI Assistant] --> Q
    S[Auto-gen Flashcards] --> Q
```

## Data Flow - Flashcard Learning

```mermaid
sequenceDiagram
    participant U as User
    participant V as View
    participant M as Model
    participant DB as Database
    
    U->>V: Start learning session
    V->>M: Get FlashcardSet
    M->>DB: Query flashcards
    DB-->>M: Return cards
    M-->>V: Flashcard list
    V-->>U: Show first card
    
    U->>V: Flip card (Space key)
    V-->>U: Show answer
    
    U->>V: Mark as learned (1 key)
    V->>M: Update FlashcardProgress
    M->>DB: Set is_learned=True
    DB-->>M: Confirm
    M-->>V: Success
    V-->>U: Next card
```

## Module Relationships

```mermaid
graph TD
    subgraph Core
        A[kien_thuc]
        B[de_thi]
        C[nguoi_dung]
    end
    
    subgraph Features
        D[studio]
        E[leaderboard]
        F[notifications]
        G[study_groups]
    end
    
    subgraph AI
        H[recommendations]
        I[ai_assistant]
    end
    
    A --> D
    A --> E
    A --> F
    A --> G
    A --> H
    
    B --> D
    B --> E
    B --> F
    B --> G
    B --> H
    
    C --> D
    C --> E
    C --> F
    C --> G
    C --> H
    
    H --> I
    
    style A fill:#e1f5ff
    style B fill:#e1f5ff
    style C fill:#e1f5ff
    style D fill:#fff4e1
    style E fill:#fff4e1
    style F fill:#fff4e1
    style G fill:#fff4e1
    style H fill:#ffe1f5
    style I fill:#ffe1f5
```

## User Journey - Learning Flow

```mermaid
journey
    title Student Learning Journey
    section Discovery
      Browse subjects: 5: Student
      Find flashcard set: 5: Student
      Preview content: 4: Student
    section Learning
      Start learning: 5: Student
      Review cards: 4: Student
      Rate difficulty: 4: Student
    section Practice
      Take practice exam: 5: Student
      Review mistakes: 4: Student
      Ask in forum: 3: Student
    section Mastery
      Complete all reviews: 5: Student
      Earn badge: 5: Student
      Climb leaderboard: 5: Student
    section Social
      Join study group: 4: Student
      Share progress: 4: Student
      Help others: 5: Student
```

## Database Schema - Phase 1 Additions

```mermaid
erDiagram
    FlashcardProgress ||--|| Flashcard : reviews
    FlashcardProgress ||--|| User : tracks
    FlashcardProgress {
        int id
        int user_id
        int flashcard_id
        float ease_factor
        int interval
        int repetition_count
        datetime next_review_date
        datetime last_review_date
        int last_quality
        boolean is_learned
    }
    
    Leaderboard ||--o{ LeaderboardEntry : contains
    LeaderboardEntry ||--|| User : ranks
    Leaderboard {
        int id
        string period
        string category
        int mon_id
        json rankings
        datetime last_updated
    }
    
    LeaderboardEntry {
        int id
        int user_id
        int leaderboard_id
        float score
        int rank
    }
    
    Notification ||--|| User : notifies
    Notification {
        int id
        int recipient_id
        int sender_id
        string notification_type
        string title
        text message
        string link
        boolean is_read
        datetime created_at
    }
```

## State Machine - Flashcard Learning

```mermaid
stateDiagram-v2
    [*] --> New
    New --> Learning: First review
    Learning --> Young: Quality >= 3
    Learning --> Learning: Quality < 3
    Young --> Mature: Interval > 21 days
    Young --> Learning: Lapse
    Mature --> Mature: Successful review
    Mature --> Young: Lapse
    Mature --> [*]: Mastered
```

## Deployment Architecture

```mermaid
graph TB
    subgraph Internet
        A[Users]
    end
    
    subgraph Load Balancer
        B[Nginx]
    end
    
    subgraph Application Servers
        C[Gunicorn 1]
        D[Gunicorn 2]
        E[Gunicorn 3]
    end
    
    subgraph Background Workers
        F[Celery Worker 1]
        G[Celery Worker 2]
        H[Celery Beat]
    end
    
    subgraph Data
        I[(PostgreSQL Primary)]
        J[(PostgreSQL Replica)]
        K[(Redis)]
    end
    
    subgraph Storage
        L[Static Files CDN]
        M[Media Storage S3]
    end
    
    A --> B
    B --> C
    B --> D
    B --> E
    
    C --> I
    D --> I
    E --> I
    
    C --> K
    D --> K
    E --> K
    
    F --> I
    G --> I
    H --> I
    
    F --> K
    G --> K
    H --> K
    
    I --> J
    
    C --> L
    D --> L
    E --> L
    
    C --> M
    D --> M
    E --> M
```

## Priority Matrix

```mermaid
quadrantChart
    title Feature Priority Matrix
    x-axis Low Effort --> High Effort
    y-axis Low Impact --> High Impact
    quadrant-1 Plan Carefully
    quadrant-2 Do First
    quadrant-3 Fill-ins
    quadrant-4 Quick Wins
    
    Spaced Repetition: [0.7, 0.9]
    Leaderboard: [0.5, 0.8]
    Notifications: [0.4, 0.7]
    Study Groups: [0.6, 0.7]
    User Following: [0.3, 0.5]
    PWA: [0.5, 0.6]
    AI Recommendations: [0.8, 0.8]
    AI Assistant: [0.9, 0.7]
    Auto-gen Cards: [0.7, 0.6]
    Dark Mode: [0.2, 0.4]
    Performance: [0.6, 0.5]
```

---

*Các diagram này giúp visualize roadmap và kiến trúc hệ thống một cách trực quan.*
