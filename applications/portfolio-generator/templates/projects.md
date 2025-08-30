---
layout: page  
title: "Projects"
description: "A showcase of my technical projects and contributions"
---

# My Projects

Here's a selection of projects that demonstrate my technical skills and problem-solving approach. Each project represents a unique challenge and learning opportunity.

{% for project in site.data.projects %}
<div class="project-card">
    <div class="project-header">
        <h3><a href="{{ project.url }}" target="_blank">{{ project.name }}</a></h3>
        <div class="project-links">
            {% if project.url %}
            <a href="{{ project.url }}" target="_blank" class="project-link">View Code</a>
            {% endif %}
            {% if project.demo %}
            <a href="{{ project.demo }}" target="_blank" class="project-link">Live Demo</a>
            {% endif %}
        </div>
    </div>
    
    <p class="project-description">{{ project.description }}</p>
    
    <div class="tech-stack">
        <h4>Technologies Used:</h4>
        <div class="tech-tags">
            {% for tech in project.tech %}
            <span class="tech-tag">{{ tech }}</span>
            {% endfor %}
        </div>
    </div>
    
    {% if project.highlights %}
    <div class="project-highlights">
        <h4>Key Features:</h4>
        <ul>
        {% for highlight in project.highlights %}
            <li>{{ highlight }}</li>
        {% endfor %}
        </ul>
    </div>
    {% endif %}
</div>
{% endfor %}

## Open Source Contributions

I believe in contributing back to the developer community. Here are some of my notable contributions to open source projects:

- **Community Impact**: Contributed to various projects improving developer tools and libraries
- **Documentation**: Enhanced project documentation to help onboard new contributors  
- **Bug Fixes**: Identified and resolved issues in popular frameworks and tools
- **Feature Development**: Implemented new features based on community needs

## Technical Writing

I enjoy sharing knowledge through technical writing:

- Blog posts on development best practices and emerging technologies
- Tutorials and guides for complex technical implementations
- Documentation for projects and tools I've developed

[View My Blog →]({{ site.author.blog | default: '#' }})

---

Want to collaborate on a project? [Let's talk!]({{ '/contact' | relative_url }})