---
layout: default
title: Schedule — Foundations of Data Science
active_tab: schedule
---

# Schedule

<div class="alert alert-info">
 14 You can <a href="https://brynmawr.hosted.panopto.com/Panopto/Pages/Sessions/List.aspx?folderID=430366e5-ac90-4388-8501-b4b800ded140">
watch recordings of the Fall 2026 lecture videos online</a>. These recordings require a BMC/HC login.
</div>

The schedule is tentative and will be updated as the term progresses. Complete each week’s reading before Tuesday’s lecture unless otherwise announced.


{% for week in site.data.schedule %}
<h3>{{ week.name }}</h3>

<table class="table table-striped">
  <thead>
    <tr>
      <th>Date</th>
      <th>Topic</th>
      <th>Reading</th>
      <th>Assignments</th>
    </tr>
  </thead>
  <tbody>
  {% for meeting in week.lectures %}
    <tr{% if meeting.type == 'no_lecture' %} class="success"{% endif %}>
      <td>{{ meeting.date | date: '%a, %b %-d, %Y' }}</td>
      <td>
        {{ meeting.title }}
        {% if meeting.slides %}
          <br><a href="{{ meeting.slides | relative_url }}">[slides]</a>
        {% endif %}
        {% if meeting.handouts %}
          <br><a href="{{ meeting.handouts | relative_url }}">[handout]</a>
        {% endif %}
      </td>
      <td>
        {% for reading in meeting.readings %}
          {% if reading.optional %}<strong>Optional:</strong> {% endif %}
          {% if reading.url %}<a href="{{ reading.url }}">{{ reading.title }}</a>{% else %}{{ reading.title }}{% endif %}
          {% unless forloop.last %}<br>{% endunless %}
        {% endfor %}
      </td>
      <td>
        {% for assignment in meeting.assignments %}
          {% if assignment.url %}<a href="{{ assignment.url | relative_url }}">{{ assignment.title }}</a>{% else %}{{ assignment.title }}{% endif %}
          {% if assignment.deadline %}<br><small>Due: {{ assignment.deadline }}</small>{% endif %}
          {% unless forloop.last %}<br>{% endunless %}
        {% endfor %}
      </td>
    </tr>
  {% endfor %}
  </tbody>
</table>
{% endfor %}
