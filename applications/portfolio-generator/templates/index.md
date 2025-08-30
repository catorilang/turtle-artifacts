---
layout: page
title: "Welcome"
description: "Professional portfolio showcasing my projects and expertise"
---

# Hello, I'm {{ site.author.name }}

## {{ site.author.title }}

Welcome to my professional portfolio. I'm a passionate developer with expertise in building scalable applications and solving complex technical challenges.

### What I Do

I specialize in creating robust, user-friendly applications using modern technologies. My experience spans across full-stack development, with a focus on clean code, performance optimization, and exceptional user experiences.

### Featured Projects

{% for project in site.data.projects limit:3 %}
<div class="featured-project">
    <h4><a href="{{ project.url }}" target="_blank">{{ project.name }}</a></h4>
    <p>{{ project.description }}</p>
    <div class="tech-stack">
        {% for tech in project.tech %}
        <span class="tech-tag">{{ tech }}</span>
        {% endfor %}
    </div>
</div>
{% endfor %}

[View All Projects →]({{ '/projects' | relative_url }})

### Let's Connect

Interested in collaborating or learning more about my work? I'd love to hear from you.

- 📧 [{{ site.author.email }}](mailto:{{ site.author.email }})
- 💼 [LinkedIn](https://linkedin.com/in/{{ site.author.linkedin }})
- 🚀 [GitHub](https://github.com/{{ site.author.github }})

[Get In Touch →]({{ '/contact' | relative_url }})