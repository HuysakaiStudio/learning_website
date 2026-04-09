# Comprehensive Development Roadmap

## 1. Flashcard System (Core: Organization & Insights)
- **User-generated Tags/Categories**: Foundational for content management.
- **Progress Dashboard**: Visualize learning efficacy using Chart.js.
- **Export/Share**: CSV/JSON export and unique public sharing links.

## 2. User Profile & Gamification (Core: Engagement & Retention)
- **Comprehensive Profile**: History, detailed performance stats, and settings.
- **Analytics Integration**: Directly embed existing performance metrics into the User Profile dashboard.
- **Challenge Engine (Badges)**: 
    - **Implementation**: Signal-based system (`post_save`) on `KetQua`.
    - **Badge Categories**: 
        - **Training Badges**: Awarded for consistency and volume in "Luyện tập" mode.
        - **Exam Badges**: Awarded for excellence in "Thi thật" mode (e.g., scoring > 8.0/10.0 within the time limit).
    - **Logic**: Use `che_do` (exam mode) and `diem` (score) to trigger specific badges.
- **Balancing Strategy**: Tiered system (Bronze/Silver/Gold) to ensure accessibility for all learners.

## Roadmap & Priorities
1. **Flashcard Tags**: High (Foundation).
2. **Profile & History**: High (Foundation).
3. **Analytics Dashboard**: Medium (Insight).
4. **Achievement Badges (Challenge Engine)**: Medium/Long-term (Retention).
5. **Export & Sharing**: Low (Portability).

## Feasibility Notes
- **Automation**: Use signals for real-time achievement tracking.
- **Performance**: Cache aggregate analytics to keep the dashboard snappy.
- **Scalability**: Tiered badges ensure low-barrier entry for new users and high-skill targets for power users.
