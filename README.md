<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prantik Medhi | Full Stack Developer</title>
    <style>
        /* --- RESET & BASICS --- */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            /* 'pixelated' is good for retro vibes, but ensure your images support it */
            image-rendering: pixelated; 
            image-rendering: -moz-crisp-edges;
            image-rendering: crisp-edges;
        }

        html {
            scroll-behavior: smooth;
            overflow-x: hidden; /* Prevents horizontal scrollbar issues */
        }

        body {
            font-family: 'Courier New', monospace;
            background: #1a1410;
            color: #f5dcc8;
            line-height: 1.6;
            overflow-x: hidden;
        }

        /* --- NAVIGATION --- */
        nav {
            position: fixed;
            top: 0;
            width: 100%;
            background: #1a1410;
            padding: 20px 40px;
            z-index: 1000;
            box-shadow: 0 2px 0 #ff8c42;
        }

        nav ul {
            list-style: none;
            display: flex;
            justify-content: center;
            gap: 40px;
            align-items: center;
        }

        nav a {
            color: #f5dcc8;
            text-decoration: none;
            font-size: 14px;
            transition: color 0.3s;
            position: relative;
        }

        nav a::after {
            content: '';
            position: absolute;
            bottom: -4px;
            left: 0;
            width: 0;
            height: 2px;
            background: #ff8c42;
            transition: width 0.3s;
        }

        nav a:hover {
            color: #ff8c42;
        }

        nav a:hover::after {
            width: 100%;
        }

        .hire-btn {
            padding: 8px 20px;
            background: #ff8c42;
            color: #1a1410 !important;
            box-shadow: 3px 3px 0 #d97132;
        }

        .hire-btn:hover {
            background: #ff9f5e;
            transform: translate(-1px, -1px);
            box-shadow: 4px 4px 0 #d97132;
        }

        .hire-btn::after {
            display: none;
        }

        /* --- HERO SECTION --- */
        .hero {
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 100px 20px 80px;
            position: relative;
            background: 
                repeating-linear-gradient(
                    0deg,
                    transparent,
                    transparent 4px,
                    rgba(255, 140, 66, 0.02) 4px,
                    rgba(255, 140, 66, 0.02) 8px
                ),
                repeating-linear-gradient(
                    90deg,
                    transparent,
                    transparent 4px,
                    rgba(255, 140, 66, 0.02) 4px,
                    rgba(255, 140, 66, 0.02) 8px
                );
        }

        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 20px;
            background: #2a1f18;
            border: 2px solid #ff8c42;
            color: #ff8c42;
            font-size: 12px;
            margin-bottom: 30px;
            box-shadow: 3px 3px 0 rgba(255, 140, 66, 0.3);
        }

        .status-dot {
            width: 8px;
            height: 8px;
            background: #ff8c42;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.3; }
        }

        h1 {
            font-size: 56px;
            margin: 20px 0;
            color: #fff;
            font-weight: 700;
            letter-spacing: 2px;
            text-shadow: 4px 4px 0 rgba(255, 140, 66, 0.3);
        }

        h1 strong {
            color: #ff8c42;
        }

        .subtitle {
            font-size: 16px;
            color: #c9a98a;
            max-width: 700px;
            margin: 20px auto;
        }

        .cta-buttons {
            display: flex;
            gap: 20px;
            margin-top: 40px;
        }

        .btn {
            padding: 14px 32px;
            font-size: 14px;
            font-family: 'Courier New', monospace;
            border: 2px solid;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            transition: all 0.2s;
            font-weight: 700;
            box-shadow: 4px 4px 0 rgba(0, 0, 0, 0.3);
        }

        .btn-primary {
            background: #ff8c42;
            border-color: #ff8c42;
            color: #1a1410;
        }

        .btn-primary:hover {
            background: #ff9f5e;
            transform: translate(-2px, -2px);
            box-shadow: 6px 6px 0 rgba(0, 0, 0, 0.3);
        }

        .btn-secondary {
            background: transparent;
            border-color: #ff8c42;
            color: #ff8c42;
        }

        .btn-secondary:hover {
            background: rgba(255, 140, 66, 0.1);
            transform: translate(-2px, -2px);
            box-shadow: 6px 6px 0 rgba(255, 140, 66, 0.3);
        }

        section {
            padding: 100px 40px;
            max-width: 1200px;
            margin: 0 auto;
        }

        h2 {
            font-size: 36px;
            margin-bottom: 50px;
            color: #ff8c42;
            text-align: center;
            font-weight: 700;
            text-shadow: 3px 3px 0 rgba(255, 140, 66, 0.2);
        }

        .section-subtitle {
            text-align: center;
            color: #c9a98a;
            font-size: 16px;
            margin-top: -30px;
            margin-bottom: 50px;
        }

        /* --- ABOUT SECTION --- */
        .about-content {
            display: grid;
            grid-template-columns: 1.5fr 1fr;
            gap: 60px;
            align-items: start;
        }

        .about-text p {
            font-size: 15px;
            line-height: 1.8;
            color: #e5c9ad;
            margin-bottom: 20px;
        }

        .about-text strong {
            color: #ff8c42;
        }

        .skills-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
        }

        .skill-box {
            padding: 20px;
            background: #2a1f18;
            border: 2px solid #ff8c42;
            text-align: center;
            font-size: 12px;
            color: #ff8c42;
            transition: all 0.2s;
            font-weight: 700;
            box-shadow: 3px 3px 0 rgba(255, 140, 66, 0.3);
        }

        .skill-box:hover {
            background: rgba(255, 140, 66, 0.1);
            transform: translate(-2px, -2px);
            box-shadow: 5px 5px 0 rgba(255, 140, 66, 0.3);
        }

        /* --- SERVICES SECTION --- */
        .services-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 24px;
        }

        .service-card {
            background: #2a1f18;
            border: 2px solid #ff8c42;
            padding: 32px;
            transition: all 0.2s;
            position: relative;
            box-shadow: 4px 4px 0 rgba(255, 140, 66, 0.3);
        }

        .service-card:hover {
            transform: translate(-2px, -2px);
            box-shadow: 6px 6px 0 rgba(255, 140, 66, 0.3);
        }

        .service-number {
            position: absolute;
            top: 20px;
            right: 20px;
            font-size: 48px;
            color: rgba(255, 140, 66, 0.15);
            font-weight: 700;
        }

        .service-card h3 {
            font-size: 18px;
            color: #ff8c42;
            margin-bottom: 16px;
            font-weight: 700;
        }

        .service-card p {
            font-size: 13px;
            line-height: 1.7;
            color: #c9a98a;
            margin-bottom: 20px;
        }

        .badge {
            display: inline-block;
            padding: 6px 12px;
            background: rgba(106, 255, 130, 0.2);
            border: 2px solid #6aff82;
            color: #6aff82;
            font-size: 11px;
            font-weight: 700;
            box-shadow: 2px 2px 0 rgba(106, 255, 130, 0.3);
        }

        /* --- PROJECTS SECTION --- */
        .projects-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 32px;
        }

        .project-card {
            background: #2a1f18;
            border: 2px solid #ff8c42;
            overflow: hidden;
            transition: all 0.2s;
            box-shadow: 4px 4px 0 rgba(255, 140, 66, 0.3);
        }

        .project-card:hover {
            transform: translate(-2px, -2px);
            box-shadow: 6px 6px 0 rgba(255, 140, 66, 0.3);
        }

        .project-image {
            width: 100%;
            height: 200px;
            background: linear-gradient(135deg, #3a2f28 0%, #2a1f18 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 48px;
            border-bottom: 2px solid #ff8c42;
        }

        /* Image object-fit fix for actual images */
        .project-image img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        .project-content {
            padding: 28px;
        }

        .project-tag {
            font-size: 11px;
            color: #ff8c42;
            margin-bottom: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 700;
        }

        .project-card h3 {
            font-size: 18px;
            color: #fff;
            margin-bottom: 12px;
            font-weight: 700;
        }

        .project-card p {
            font-size: 13px;
            line-height: 1.7;
            color: #c9a98a;
            margin-bottom: 20px;
        }

        .tech-tags {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-bottom: 20px;
        }

        .tech-tag {
            padding: 6px 12px;
            background: transparent;
            border: 2px solid #ff8c42;
            font-size: 11px;
            color: #ff8c42;
            box-shadow: 2px 2px 0 rgba(255, 140, 66, 0.3);
        }

        /* --- TESTIMONIALS --- */
        .testimonials {
            background: #0f0b08;
            padding: 80px 40px;
            border-top: 2px solid #ff8c42;
            border-bottom: 2px solid #ff8c42;
        }

        .testimonials-container {
            max-width: 1200px;
            margin: 0 auto;
            overflow: hidden; /* Important for the JS scroll to work cleanly */
        }

        .testimonials-scroll {
            display: flex;
            overflow-x: auto; /* changed from hidden to auto for fallback, JS handles scroll */
            gap: 32px;
            padding: 20px 0;
            user-select: none;
            scrollbar-width: none; /* Hide scrollbar Firefox */
        }
        
        .testimonials-scroll::-webkit-scrollbar {
            display: none; /* Hide scrollbar Chrome/Safari */
        }

        .testimonial-card {
            flex: 0 0 400px;
            background: #2a1f18;
            border: 2px solid #ff8c42;
            padding: 32px;
            box-shadow: 4px 4px 0 rgba(255, 140, 66, 0.3);
        }

        .testimonial-text {
            font-size: 14px;
            line-height: 1.8;
            color: #e5c9ad;
            margin-bottom: 24px;
        }

        .testimonial-author {
            display: flex;
            align-items: center;
            gap: 16px;
        }

        .author-avatar {
            width: 48px;
            height: 48px;
            background: #ff8c42;
            border: 2px solid #d97132;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            color: #1a1410;
            font-weight: 700;
        }

        .author-info h4 {
            font-size: 14px;
            color: #ff8c42;
            margin-bottom: 4px;
            font-weight: 700;
        }

        .author-info p {
            font-size: 12px;
            color: #c9a98a;
        }

        .scroll-hint {
            text-align: center;
            color: #8a6f5a;
            font-size: 12px;
            margin-top: 20px;
        }

        /* --- CONTACT & FOOTER --- */
        .contact-form {
            max-width: 600px;
            margin: 0 auto; /* Fixed typo: removed 'чувство' */
        }

        .form-group {
            margin-bottom: 24px;
        }

        label {
            display: block;
            font-size: 13px;
            margin-bottom: 8px;
            color: #ff8c42;
            font-weight: 700;
        }

        input, textarea {
            width: 100%;
            padding: 14px 16px;
            background: #2a1f18;
            border: 2px solid #ff8c42;
            color: #f5dcc8;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            transition: all 0.3s;
        }

        input:focus, textarea:focus {
            outline: none;
            background: #3a2f28;
            box-shadow: 0 0 0 3px rgba(255, 140, 66, 0.3);
        }

        textarea {
            min-height: 150px;
            resize: vertical;
        }

        footer {
            text-align: center;
            padding: 60px 20px;
            border-top: 2px solid #ff8c42;
            font-size: 13px;
            color: #8a6f5a;
        }

        .contact-buttons {
            display: flex;
            flex-wrap: wrap;
            gap: 32px;
            justify-content: center;
            margin: 0 auto;
            max-width: 900px;
        }

        .contact-btn {
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 40px 50px;
            background: #2a1f18;
            border: 2px solid #ff8c42;
            text-decoration: none;
            color: #ff8c42;
            font-family: 'Courier New', monospace;
            font-size: 18px;
            font-weight: 700;
            letter-spacing: 1px;
            min-width: 220px;
            transition: all 0.2s;
            box-shadow: 4px 4px 0 rgba(255, 140, 66, 0.3);
        }

        .contact-btn:hover {
            transform: translate(-2px, -2px);
            box-shadow: 6px 6px 0 rgba(255, 140, 66, 0.3);
            background: rgba(255, 140, 66, 0.05);
            color: #ff9f5e;
        }

        /* --- MEDIA QUERIES --- */
        @media (max-width: 768px) {
            nav {
                padding: 15px 20px;
            }
            nav ul {
                gap: 20px;
                font-size: 12px;
                flex-wrap: wrap;
            }
            h1 {
                font-size: 36px;
            }
            h2 {
                font-size: 28px;
            }
            .about-content {
                grid-template-columns: 1fr;
            }
            .skills-grid {
                grid-template-columns: 1fr;
            }
            .cta-buttons {
                flex-direction: column;
                width: 100%;
            }
            .btn {
                width: 100%;
                text-align: center;
            }
            section {
                padding: 60px 20px;
            }
            .testimonial-card {
                flex: 0 0 300px;
            }
            .contact-buttons {
                flex-direction: column;
                align-items: center;
            }
            .contact-btn {
                width: 100%;
                max-width: 320px;
                padding: 35px 50px;
            }
        }
    </style>
</head>
<body>
    <nav>
        <ul>
            <li><a href="#home">Home</a></li>
            <li><a href="#about">About</a></li>
            <li><a href="#services">Services</a></li>
            <li><a href="#projects">Projects</a></li>
            <li><a href="#contact" class="hire-btn">Hire Me</a></li>
        </ul>
    </nav>

    <section id="home" class="hero">
        <div class="status-badge">
            <span class="status-dot"></span>
            Available for new projects
        </div>
        <h1>Innovating Beyond<br>Digital Limits</h1>
        <p class="subtitle">
            Hi, I'm <strong>Prantik Medhi</strong>. A Full Stack Developer crafting modern, high-performance web applications with a focus on clean design and user experience.
        </p>
        <div class="cta-buttons">
            <a href="#projects" class="btn btn-primary">View Work</a>
            <a href="#contact" class="btn btn-secondary">Contact Me</a>
        </div>
    </section>

    <section id="about">
        <h2>About Me</h2>
        <div class="about-content">
            <div class="about-text">
                <p>I'm a young and passionate <strong>Full Stack Developer</strong> based in India. I specialize in building fast, modern, and accessible websites that not only look premium but perform flawlessly.</p>
                <p>My approach combines strong <strong>UI/UX thinking</strong> with clean code. I don't just write software; I craft digital experiences that solve real problems while feeling intuitive and luxurious to use.</p>
                <p>With expertise in the React ecosystem and a love for AI/ML, I'm constantly exploring new ways to make the web more intelligent and interactive.</p>
            </div>
            <div class="skills-grid">
                <div class="skill-box">Clean Code</div>
                <div class="skill-box">Premium UI</div>
                <div class="skill-box">Fast Performance</div>
                <div class="skill-box">Responsive</div>
            </div>
        </div>
    </section>

    <section id="services">
        <h2>Solutions for the Modern Era</h2>
        <p class="section-subtitle">I combine creativity with technical excellence to deliver results that matter.</p>
        <div class="services-grid">
            <div class="service-card">
                <span class="service-number">01</span>
                <h3>Video Editing</h3>
                <p>Professional editing that transforms raw footage into compelling stories. I handle color grading, sound design, and motion graphics to make your content shine.</p>
                <span class="badge">Available Now</span>
            </div>
            <div class="service-card">
                <span class="service-number">02</span>
                <h3>Graphic Design</h3>
                <p>Eye-catching visual identities, marketing materials, and social media assets. My designs are tailored to communicate your brand's message effectively.</p>
                <span class="badge">Available Now</span>
            </div>
            <div class="service-card">
                <span class="service-number">03</span>
                <h3>Website Design</h3>
                <p>Modern, responsive, and performance-focused websites. I create digital experiences that look great and convert visitors into customers.</p>
                <span class="badge">Available Now</span>
            </div>
            <div class="service-card">
                <span class="service-number">04</span>
                <h3>AI Lead Gen</h3>
                <p>Leverage the power of AI to automate your lead generation. I build systems that find and qualify your ideal prospects around the clock.</p>
                <span class="badge">Available Now</span>
            </div>
        </div>
    </section>

    <section id="projects">
        <h2>My Work</h2>
        <p class="section-subtitle">A showcase of my best projects and experiments.</p>
        <div class="projects-grid">
            <div class="project-card">
                <div class="project-image">
                    <img src="/src/hospital.png" alt="Hospital Management System preview">
                </div>
                <div class="project-content">
                    <div class="project-tag">Web App</div>
                    <h3>Hospital Management System</h3>
                    <p>A comprehensive platform for managing hospital operations, patient records, and appointments.</p>
                    <div class="tech-tags">
                        <span class="tech-tag">Next.js</span>
                        <span class="tech-tag">PostgreSQL</span>
                        <span class="tech-tag">Tailwind</span>
                    </div>
                    <a href="https://mirzamultispecialityhospital.in" class="btn btn-primary" target="_blank">View Project</a>
                </div>
            </div>
            <div class="project-card">
                <div class="project-image">
                    <img src="/src/kip.png" alt="Kish Investment Park website preview">
                </div>
                <div class="project-content">
                    <div class="project-tag">Corporate Site</div>
                    <h3>Kish Investment Park</h3>
                    <p>Premium investment portal designed with modern aesthetics and robust functionality.</p>
                    <div class="tech-tags">
                        <span class="tech-tag">HTML</span>
                        <span class="tech-tag">Framer Motion</span>
                        <span class="tech-tag">CMS</span>
                    </div>
                    <a href="http://kiship.com" class="btn btn-primary" target="_blank">View Project</a>
                </div>
            </div>
            <div class="project-card">
                <div class="project-image">
                    <img src="/src/sawarias01.png" alt="SAWARI AS-01 Rentals website preview">
                </div>
                <div class="project-content">
                    <div class="project-tag">Business Service</div>
                    <h3>SAWARI AS-01 Rentals</h3>
                    <p>Vehicle-rental portal offering cars, bikes & scooters for hourly, daily, weekly or monthly bookings — with clean UI, smooth navigation, and clear service listings.</p>
                    <div class="tech-tags">
                        <span class="tech-tag">Next.js</span>
                        <span class="tech-tag">Tailwind</span>
                        <span class="tech-tag">Responsive UI</span>
                    </div>
                    <a href="https://sawarias01.in" class="btn btn-primary" target="_blank">View Project</a>
                </div>
            </div>
        </div>
    </section>

    <div class="testimonials">
        <div class="testimonials-container">
            <h2>Client Testimonials</h2>
            <div class="testimonials-scroll" id="testimonialScroll">
                <div class="testimonial-card">
                    <p class="testimonial-text">"Prantik is a rare talent who bridges the gap between engineering and design perfectly. The platform he built for us exceeded all expectations in performance and aesthetics."</p>
                    <div class="testimonial-author">
                        <div class="author-avatar">SJ</div>
                        <div class="author-info">
                            <h4>Sarah Jenkins</h4>
                            <p>CTO, TechFlow</p>
                        </div>
                    </div>
                </div>
                <div class="testimonial-card">
                    <p class="testimonial-text">"Working with Prantik was seamless. He understood our vision immediately and delivered a high-end product that helped us secure our Series A funding."</p>
                    <div class="testimonial-author">
                        <div class="author-avatar">MC</div>
                        <div class="author-info">
                            <h4>Michael Chen</h4>
                            <p>Founder, StartScale</p>
                        </div>
                    </div>
                </div>
                <div class="testimonial-card">
                    <p class="testimonial-text">"The attention to detail in the UI interactions is unmatched. Prantik doesn't just build websites; he builds experiences that users love."</p>
                    <div class="testimonial-author">
                        <div class="author-avatar">ER</div>
                        <div class="author-info">
                            <h4>Elena Rodriguez</h4>
                            <p>Product Director, Nova</p>
                        </div>
                    </div>
                </div>
                <div class="testimonial-card">
                    <p class="testimonial-text">"Exceptional code quality and communication. He delivered the project ahead of schedule and the final result was polished to perfection."</p>
                    <div class="testimonial-author">
                        <div class="author-avatar">DW</div>
                        <div class="author-info">
                            <h4>David Wright</h4>
                            <p>CEO, BrightWeb</p>
                        </div>
                    </div>
                </div>
                <div class="testimonial-card">
                    <p class="testimonial-text">"The dashboard metrics are now crystal clear. The data visualization work Prantik did for our internal tools has completely transformed how we track KPIs."</p>
                    <div class="testimonial-author">
                        <div class="author-avatar">JW</div>
                        <div class="author-info">
                            <h4>James Wilson</h4>
                            <p>Marketing Lead, GrowthCo</p>
                        </div>
                    </div>
                </div>
                <div class="testimonial-card">
                    <p class="testimonial-text">"Prantik is a rare talent who bridges the gap between engineering and design perfectly. The platform he built for us exceeded all expectations in performance and aesthetics."</p>
                    <div class="testimonial-author">
                        <div class="author-avatar">SJ</div>
                        <div class="author-info">
                            <h4>Sarah Jenkins</h4>
                            <p>CTO, TechFlow</p>
                        </div>
                    </div>
                </div>
                <div class="testimonial-card">
                    <p class="testimonial-text">"Working with Prantik was seamless. He understood our vision immediately and delivered a high-end product that helped us secure our Series A funding."</p>
                    <div class="testimonial-author">
                        <div class="author-avatar">MC</div>
                        <div class="author-info">
                            <h4>Michael Chen</h4>
                            <p>Founder, StartScale</p>
                        </div>
                    </div>
                </div>
                <div class="testimonial-card">
                    <p class="testimonial-text">"The attention to detail in the UI interactions is unmatched. Prantik doesn't just build websites; he builds experiences that users love."</p>
                    <div class="testimonial-author">
                        <div class="author-avatar">ER</div>
                        <div class="author-info">
                            <h4>Elena Rodriguez</h4>
                            <p>Product Director, Nova</p>
                        </div>
                    </div>
                </div>
                <div class="testimonial-card">
                    <p class="testimonial-text">"Exceptional code quality and communication. He delivered the project ahead of schedule and the final result was polished to perfection."</p>
                    <div class="testimonial-author">
                        <div class="author-avatar">DW</div>
                        <div class="author-info">
                            <h4>David Wright</h4>
                            <p>CEO, BrightWeb</p>
                        </div>
                    </div>
                </div>
                <div class="testimonial-card">
                    <p class="testimonial-text">"The dashboard metrics are now crystal clear. The data visualization work Prantik did for our internal tools has completely transformed how we track KPIs."</p>
                    <div class="testimonial-author">
                        <div class="author-avatar">JW</div>
                        <div class="author-info">
                            <h4>James Wilson</h4>
                            <p>Marketing Lead, GrowthCo</p>
                        </div>
                    </div>
                </div>
            </div>
            <p class="scroll-hint">Auto-scrolling • Hover to pause</p>
        </div>
    </div>

    <section id="contact">
        <h2>Let's Connect</h2>
        <p class="section-subtitle">Feel free to reach out—I'm always open to discussing new opportunities or ideas.</p>
        
        <div class="contact-buttons">
            <a href="https://in.linkedin.com/in/prantikmedhi" target="_blank" class="contact-btn">
                LinkedIn
            </a>
            
            <a href="mailto:prantikpratimmedhi@gmail.com" class="contact-btn">
                Email Me!
            </a>
            
            <a href="https://github.com/prantikmedhi" target="_blank" class="contact-btn">
                GitHub
            </a>
        </div>
    </section>

    <footer>
        <p>© 2025 Prantik Medhi. All rights reserved.</p>
    </footer>

    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const container = document.getElementById('testimonialScroll');
            let isPaused = false;
            let animationId;
        
            const scroll = () => {
                if (!isPaused && container) {
                    container.scrollLeft += 1;
        
                    // Check if we've scrolled past half the content (assuming duplicate content for loop)
                    if (container.scrollLeft >= (container.scrollWidth - container.clientWidth)) {
                        container.scrollLeft = 0;
                    }
                }
                animationId = requestAnimationFrame(scroll);
            };
        
            if (container) {
                container.addEventListener('mouseenter', () => isPaused = true);
                container.addEventListener('mouseleave', () => isPaused = false);
                container.addEventListener('touchstart', () => isPaused = true);
                container.addEventListener('touchend', () => setTimeout(() => isPaused = false, 3000));
                
                scroll();
            }
        });
    </script>
</body>
</html>
