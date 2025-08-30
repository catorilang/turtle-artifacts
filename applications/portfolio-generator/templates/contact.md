---
layout: page
title: "Contact"
description: "Get in touch for collaborations, opportunities, or just to say hello"
---

# Let's Connect

I'm always interested in discussing new opportunities, collaborating on interesting projects, or simply connecting with fellow developers and technology enthusiasts.

## Get In Touch

<div class="contact-grid">
    <div class="contact-method">
        <h3>📧 Email</h3>
        <p><a href="mailto:{{ site.author.email }}">{{ site.author.email }}</a></p>
        <p>Best for: Project inquiries, collaboration proposals, detailed discussions</p>
    </div>

    <div class="contact-method">
        <h3>💼 LinkedIn</h3>
        <p><a href="https://linkedin.com/in/{{ site.author.linkedin }}" target="_blank">{{ site.author.linkedin }}</a></p>
        <p>Best for: Professional networking, career opportunities, industry connections</p>
    </div>

    <div class="contact-method">
        <h3>🚀 GitHub</h3>
        <p><a href="https://github.com/{{ site.author.github }}" target="_blank">{{ site.author.github }}</a></p>
        <p>Best for: Code collaboration, open source contributions, technical discussions</p>
    </div>

    {% if site.author.twitter %}
    <div class="contact-method">
        <h3>🐦 Twitter</h3>
        <p><a href="https://twitter.com/{{ site.author.twitter }}" target="_blank">@{{ site.author.twitter }}</a></p>
        <p>Best for: Quick questions, tech discussions, community engagement</p>
    </div>
    {% endif %}
</div>

## What I'm Looking For

### Collaboration Opportunities
- Open source project contributions
- Technical writing and documentation
- Speaking opportunities at conferences or meetups
- Mentoring and knowledge sharing

### Project Inquiries
- Full-stack web development projects
- API design and implementation
- System architecture and scalability consulting
- DevOps and cloud infrastructure setup

### Professional Opportunities
- Full-time or contract development roles
- Technical leadership positions
- Consulting and advisory roles
- Remote or hybrid work arrangements

## Current Availability

**Status**: {{ site.author.availability | default: "Open to opportunities" }}

{% if site.author.availability_details %}
{{ site.author.availability_details }}
{% else %}
I'm currently available for new projects and opportunities. Response time is typically within 24-48 hours for all inquiries.
{% endif %}

## Quick Contact Form

*Note: This form requires additional setup with a form handling service like Formspree or Netlify Forms*

<form class="contact-form" action="#" method="POST">
    <div class="form-group">
        <label for="name">Name</label>
        <input type="text" id="name" name="name" required>
    </div>
    
    <div class="form-group">
        <label for="email">Email</label>
        <input type="email" id="email" name="email" required>
    </div>
    
    <div class="form-group">
        <label for="subject">Subject</label>
        <input type="text" id="subject" name="subject" required>
    </div>
    
    <div class="form-group">
        <label for="message">Message</label>
        <textarea id="message" name="message" rows="5" required></textarea>
    </div>
    
    <button type="submit" class="submit-button">Send Message</button>
</form>

## Response Time

I aim to respond to all inquiries within 24-48 hours. For urgent matters, please mention "URGENT" in your subject line.

### Time Zone
{{ site.author.timezone | default: "Eastern Time (ET)" }}

---

Looking forward to hearing from you!