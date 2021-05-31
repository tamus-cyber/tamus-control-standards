{% for section in site.data.references.section %}
## {{ section.title }}

{% for reference in section.references %}
[{{ reference.name }}]
: {{ reference.citation }}.

{% endfor %}

{% endfor %}
