# Plain-Words Explainer: The Contact Form

## What a backend actually is

A backend is just "the part of a website that runs on someone else's
computer instead of yours." A plain static page (like the rest of my site)
is only a file — your browser downloads it and shows it to you, and nothing
about that page can *remember* anything or *do* anything after it loads. A
backend is whatever receives, stores, or acts on information after you
submit it — it's the difference between a page that displays a form and a
system that actually catches what you typed into it.

## The one feature I wired

A real contact form. A visitor types their name, email, and a message, hits
Send, and it actually reaches me — I don't have to run a server, write any
backend code, or pay for anything to make that true.

## How the data actually flows

1. **The form lives in my static HTML**, same as every other file on the
   site. Nothing about the form tag itself is special-looking — it's just
   `<form>`, `<input>`, `<textarea>`, plain HTML.

2. **One attribute changes everything**: `data-netlify="true"` on the form
   tag. When I deploy the site, Netlify's build process scans the raw HTML
   files for that attribute. Finding it tells Netlify "this form is real,
   set up a place to catch its submissions" — this scan happens once, at
   deploy time, not on every page load.

3. **When a visitor clicks Send**, the browser packages up whatever they
   typed (name, email, message) and sends it as a POST request. I wrote a
   small script so this happens in the background (so the visitor sees an
   inline "thanks" instead of the page reloading), but the actual request
   Netlify receives is identical either way — the JavaScript only changes
   what the visitor *sees*, not what gets sent.

4. **Netlify's backend — not mine — receives that POST request.** This is
   the actual backend in this feature: a service Netlify runs, that I never
   had to build, configure with a database, or write a line of server code
   for. It takes the submitted fields and stores them.

5. **The submission shows up in two places**: Netlify's dashboard (Forms
   tab), and as an email notification to whatever address I set as the
   site owner. That's the "a real submission reaches me" part — I don't
   have to log in and check a database; it lands in my inbox like a normal
   email.

6. **The honeypot field** (a hidden input named `bot-field`) is a tiny bit
   of anti-spam: real visitors can't see it and won't fill it in, but
   automated bots that blindly fill out every field on a page will — so
   Netlify silently discards any submission where that hidden field isn't
   empty, without me writing any spam-detection logic myself.

## Why this counts as "wiring a real backend feature," even with zero server code

It's tempting to think "I didn't write a backend, I just added an
attribute." But the point of the exercise isn't "did I personally write
server code" — it's "does a real system now receive, store, and act on data
after a visitor interacts with my site, instead of the page just sitting
there." Before this, my site could only ever *tell* a visitor something.
Now it can *catch* something a visitor gives it and get it to me. That's
the actual line between a poster and a tool, and Netlify Forms crosses it
without me needing to run my own server to do it.
