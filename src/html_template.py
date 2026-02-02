"""
HTML Template for the Maths Homework Generator
Separated for easier maintenance
"""

import json

def get_html_template(topics_list):
    """Generate the HTML template with topics injected"""
    topics_json = json.dumps(topics_list)

    return f'''<!DOCTYPE html>
<html lang="en" data-theme="default">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MathsForge AI</title>
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🔥</text></svg>">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        /* Default Dark Theme */
        :root, [data-theme="default"] {{
            --bg-dark: #0a0a12;
            --bg-card: #12121c;
            --bg-card-hover: #1a1a28;
            --bg-input: #1a1a26;
            --border: #2a2a3e;
            --border-hover: #3d3d5c;
            --primary: #8b5cf6;
            --primary-light: #a78bfa;
            --primary-glow: rgba(139, 92, 246, 0.3);
            --secondary: #ec4899;
            --secondary-glow: rgba(236, 72, 153, 0.25);
            --success: #10b981;
            --success-glow: rgba(16, 185, 129, 0.3);
            --danger: #ef4444;
            --warning: #f59e0b;
            --text: #f8fafc;
            --text-soft: #cbd5e1;
            --text-muted: #64748b;
            --gradient-1: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%);
            --gradient-2: linear-gradient(135deg, #10b981 0%, #14b8a6 100%);
            --gradient-3: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            --font-main: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }}

        /* Intuitive Academy Theme - Professional Blue/Cyan with gradients */
        [data-theme="intuitive"] {{
            --bg-dark: #0c1929;
            --bg-card: #132237;
            --bg-card-hover: #1a3048;
            --bg-input: #162942;
            --border: #234060;
            --border-hover: #2e5580;
            --primary: #00b4d8;
            --primary-light: #48cae4;
            --primary-glow: rgba(0, 180, 216, 0.35);
            --secondary: #0077b6;
            --secondary-glow: rgba(0, 119, 182, 0.3);
            --success: #06d6a0;
            --success-glow: rgba(6, 214, 160, 0.3);
            --danger: #ef476f;
            --warning: #ffd166;
            --text: #f0f9ff;
            --text-soft: #bae6fd;
            --text-muted: #7dd3fc;
            --gradient-1: linear-gradient(135deg, #00b4d8 0%, #0077b6 50%, #023e8a 100%);
            --gradient-2: linear-gradient(135deg, #06d6a0 0%, #00b4d8 100%);
            --gradient-3: linear-gradient(135deg, #48cae4 0%, #00b4d8 50%, #0096c7 100%);
            --font-main: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        html {{ scroll-behavior: auto; }}

        body {{
            font-family: var(--font-main);
            background: var(--bg-dark);
            color: var(--text);
            min-height: 100vh;
            line-height: 1.6;
            padding-bottom: 140px;
            overflow-x: hidden;
        }}

        /* Custom Cursor System - Hide default cursor everywhere */
        *, *::before, *::after {{
            cursor: none !important;
        }}

        a, button, input, select, textarea, label,
        [role="button"], [onclick], .clickable,
        .paper-cell, .session-cell, .topic-btn, .theme-btn,
        .difficulty-btn, .ai-process-btn, .ai-process-btn-large,
        .toggle-ms-btn, .download-btn {{
            cursor: none !important;
        }}

        .cursor-dot {{
            position: fixed;
            width: 8px;
            height: 8px;
            background: white;
            border-radius: 50%;
            pointer-events: none;
            z-index: 10001;
            transform: translate(-50%, -50%);
            transition: transform 0.15s ease;
            box-shadow: 0 0 10px rgba(59, 130, 246, 0.8), 0 0 20px rgba(59, 130, 246, 0.4);
        }}

        .cursor-dot.clicking {{
            transform: translate(-50%, -50%) scale(0.6);
        }}

        .cursor-ring {{
            position: fixed;
            width: 40px;
            height: 40px;
            border: 2px solid rgba(59, 130, 246, 0.6);
            border-radius: 50%;
            pointer-events: none;
            z-index: 10000;
            transform: translate(-50%, -50%);
            transition: width 0.3s ease, height 0.3s ease, border-color 0.3s ease, opacity 0.3s ease;
            opacity: 0.8;
        }}

        .cursor-ring.hover {{
            width: 55px;
            height: 55px;
            border-color: rgba(59, 130, 246, 0.9);
            opacity: 1;
        }}

        .cursor-ring.clicking {{
            width: 35px;
            height: 35px;
        }}

        /* Force cursor none on all form elements */
        select, select:focus, select:hover,
        input, input:focus, input:hover,
        option {{
            cursor: none !important;
        }}

        /* Dynamic cursor glow effect */
        .cursor-glow {{
            position: fixed;
            width: 400px;
            height: 400px;
            border-radius: 50%;
            background: radial-gradient(circle, var(--primary-glow) 0%, transparent 70%);
            pointer-events: none;
            z-index: 0;
            transform: translate(-50%, -50%);
            transition: opacity 0.3s ease;
            opacity: 0.6;
        }}

        /* 3D Card Effects */
        .card-3d {{
            transform-style: preserve-3d;
            perspective: 1000px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}

        .card-3d:hover {{
            transform: translateY(-5px) rotateX(2deg) rotateY(-2deg);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3), 0 0 30px var(--primary-glow);
        }}

        .card-3d-content {{
            transform: translateZ(30px);
        }}

        /* Smooth fade-in animations */
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        @keyframes slideIn {{
            from {{
                opacity: 0;
                transform: translateX(-20px);
            }}
            to {{
                opacity: 1;
                transform: translateX(0);
            }}
        }}

        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
        }}

        @keyframes shimmer {{
            0% {{ background-position: -200% center; }}
            100% {{ background-position: 200% center; }}
        }}

        .animate-fade-in {{
            animation: fadeInUp 0.5s ease-out forwards;
        }}

        .animate-slide-in {{
            animation: slideIn 0.4s ease-out forwards;
        }}

        /* Theme Switcher */
        .theme-switcher {{
            position: fixed;
            top: 1rem;
            right: 1rem;
            z-index: 1000;
            display: flex;
            gap: 0.5rem;
            background: var(--bg-card);
            padding: 0.5rem;
            border-radius: 10px;
            border: 1px solid var(--border);
            backdrop-filter: blur(10px);
        }}

        .theme-btn {{
            padding: 0.5rem 1rem;
            border: 1px solid var(--border);
            background: var(--bg-input);
            color: var(--text-soft);
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.85rem;
            font-weight: 500;
            transition: all 0.2s ease;
        }}

        .theme-btn:hover {{
            border-color: var(--primary);
            color: var(--text);
            transform: translateY(-1px);
        }}

        .theme-btn.active {{
            background: var(--gradient-1);
            border-color: transparent;
            color: white;
            box-shadow: 0 4px 15px var(--primary-glow);
        }}

        /* Background Effects */
        .bg-effects {{
            position: fixed;
            inset: 0;
            pointer-events: none;
            z-index: 0;
            overflow: hidden;
        }}

        .bg-orb {{
            position: absolute;
            border-radius: 50%;
            filter: blur(100px);
            opacity: 0.5;
            animation: float 25s ease-in-out infinite;
        }}

        .bg-orb-1 {{
            width: 700px;
            height: 700px;
            background: var(--primary);
            top: -300px;
            left: -200px;
        }}

        .bg-orb-2 {{
            width: 600px;
            height: 600px;
            background: var(--secondary);
            bottom: -200px;
            right: -150px;
            animation-delay: -10s;
        }}

        .bg-orb-3 {{
            width: 400px;
            height: 400px;
            background: var(--success);
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            animation-delay: -5s;
            opacity: 0.3;
        }}

        @keyframes float {{
            0%, 100% {{ transform: translate(0, 0) scale(1); }}
            33% {{ transform: translate(40px, -40px) scale(1.05); }}
            66% {{ transform: translate(-30px, 30px) scale(0.95); }}
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
            position: relative;
            z-index: 1;
        }}

        header {{
            text-align: center;
            margin-bottom: 2.5rem;
            padding-top: 1rem;
        }}

        header h1 {{
            font-size: 2.8rem;
            font-weight: 800;
            background: var(--gradient-1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.5rem;
            letter-spacing: -0.02em;
        }}

        header p {{
            color: var(--text-soft);
            font-size: 1.1rem;
            font-weight: 400;
        }}

        /* AI Mode Banner - Prominent Position with 3D effect */
        .ai-mode-banner {{
            background: linear-gradient(135deg, var(--primary-glow) 0%, var(--secondary-glow) 100%);
            border: 1px solid var(--primary);
            border-radius: 16px;
            padding: 1.25rem 1.5rem;
            margin-bottom: 1.5rem;
            backdrop-filter: blur(10px);
            animation: fadeInUp 0.5s ease-out;
            transform-style: preserve-3d;
            perspective: 1000px;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}

        .ai-mode-banner::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
            animation: shimmer 3s infinite;
        }}

        .ai-mode-banner:hover {{
            transform: translateY(-3px);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2), 0 0 20px var(--primary-glow);
        }}

        .ai-mode-content {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 1rem;
        }}

        .ai-mode-left {{
            display: flex;
            align-items: center;
            gap: 1rem;
        }}

        .ai-badge {{
            background: var(--gradient-1);
            color: white;
            padding: 0.3rem 0.6rem;
            border-radius: 6px;
            font-size: 0.7rem;
            font-weight: 700;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            animation: pulse 2s infinite;
        }}

        .ai-mode-info h3 {{
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--text);
            margin-bottom: 0.2rem;
        }}

        .ai-mode-info p {{
            font-size: 0.85rem;
            color: var(--text-muted);
        }}

        .ai-toggle-btn {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            background: var(--bg-input);
            border: 2px solid var(--border);
            border-radius: 30px;
            padding: 0.5rem 1rem 0.5rem 0.5rem;
            cursor: pointer;
            transition: all 0.3s ease;
        }}

        .ai-toggle-btn:hover {{
            border-color: var(--primary);
            background: var(--bg-card-hover);
        }}

        .ai-toggle-btn.active {{
            border-color: var(--primary);
            background: rgba(139, 92, 246, 0.2);
        }}

        .toggle-track {{
            width: 44px;
            height: 24px;
            background: var(--border);
            border-radius: 12px;
            position: relative;
            transition: all 0.3s ease;
        }}

        .ai-toggle-btn.active .toggle-track {{
            background: var(--gradient-1);
        }}

        .toggle-thumb {{
            position: absolute;
            top: 2px;
            left: 2px;
            width: 20px;
            height: 20px;
            background: white;
            border-radius: 50%;
            transition: all 0.3s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }}

        .ai-toggle-btn.active .toggle-thumb {{
            left: 22px;
        }}

        .toggle-label {{
            font-weight: 600;
            font-size: 0.9rem;
            color: var(--text-soft);
        }}

        .ai-toggle-btn.active .toggle-label {{
            color: var(--primary);
        }}

        .ai-disclaimer {{
            margin-top: 0.75rem;
            padding-top: 0.75rem;
            border-top: 1px solid rgba(139, 92, 246, 0.2);
            font-size: 0.8rem;
            color: var(--warning);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .ai-disclaimer.hidden {{
            display: none;
        }}

        /* Search Section with 3D effect */
        .search-section {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 2rem;
            backdrop-filter: blur(10px);
            transform-style: preserve-3d;
            perspective: 1000px;
            transition: all 0.3s ease;
        }}

        .search-section:hover {{
            transform: translateY(-4px);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2), 0 0 25px var(--primary-glow);
            border-color: var(--border-hover);
        }}

        .form-row {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 1.5rem;
            margin-bottom: 1.5rem;
        }}

        .form-group {{
            display: flex;
            flex-direction: column;
        }}

        label {{
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: var(--text-soft);
            font-size: 0.9rem;
            letter-spacing: 0.02em;
        }}

        select, input {{
            background: var(--bg-input);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 0.85rem 1rem;
            color: var(--text);
            font-family: inherit;
            font-size: 0.95rem;
            transition: all 0.2s ease;
        }}

        select:focus, input:focus {{
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px var(--primary-glow);
        }}

        /* Modern Sleek Select Dropdown */
        .custom-select {{
            position: relative;
            width: 100%;
        }}

        .custom-select-trigger {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: linear-gradient(135deg, var(--bg-input) 0%, rgba(30, 30, 50, 0.8) 100%);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 0.9rem 1.1rem;
            color: var(--text);
            font-size: 0.95rem;
            font-weight: 500;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: none;
            backdrop-filter: blur(10px);
        }}

        .custom-select-trigger:hover {{
            border-color: var(--primary);
            background: linear-gradient(135deg, var(--bg-input) 0%, rgba(139, 92, 246, 0.1) 100%);
            transform: translateY(-1px);
        }}

        .custom-select.open .custom-select-trigger {{
            border-color: var(--primary);
            box-shadow: 0 0 20px var(--primary-glow), 0 4px 15px rgba(0, 0, 0, 0.2);
            border-radius: 12px 12px 0 0;
        }}

        .custom-select-arrow {{
            font-size: 0.65rem;
            color: var(--primary);
            transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            opacity: 0.8;
        }}

        .custom-select.open .custom-select-arrow {{
            transform: rotate(180deg);
        }}

        .custom-select-options {{
            position: absolute;
            top: calc(100% - 1px);
            left: 0;
            right: 0;
            background: var(--bg-card);
            border: 1px solid var(--primary);
            border-top: none;
            border-radius: 0 0 12px 12px;
            z-index: 100;
            max-height: 0;
            overflow: hidden;
            opacity: 0;
            transform: translateY(-10px);
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            backdrop-filter: blur(15px);
        }}

        .custom-select.open .custom-select-options {{
            max-height: 280px;
            opacity: 1;
            transform: translateY(0);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
        }}

        .custom-select-option {{
            padding: 0.8rem 1.1rem;
            color: var(--text-soft);
            transition: all 0.2s ease;
            cursor: none;
            position: relative;
            border-left: 3px solid transparent;
        }}

        .custom-select-option:hover {{
            background: linear-gradient(90deg, rgba(139, 92, 246, 0.15) 0%, transparent 100%);
            color: var(--text);
            border-left-color: var(--primary);
            padding-left: 1.3rem;
        }}

        .custom-select-option.selected {{
            background: linear-gradient(90deg, rgba(139, 92, 246, 0.2) 0%, transparent 100%);
            color: var(--primary-light);
            font-weight: 500;
            border-left-color: var(--primary);
        }}

        .custom-select-option:last-child {{
            border-radius: 0 0 12px 12px;
        }}

        /* Topic Grid */
        .topic-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 0.75rem;
            margin-top: 1rem;
            max-height: 350px;
            overflow-y: auto;
            padding-right: 0.5rem;
        }}

        .topic-grid::-webkit-scrollbar {{
            width: 6px;
        }}

        .topic-grid::-webkit-scrollbar-track {{
            background: var(--bg-input);
            border-radius: 3px;
        }}

        .topic-grid::-webkit-scrollbar-thumb {{
            background: var(--border);
            border-radius: 3px;
        }}

        .topic-item {{
            background: var(--bg-input);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 0.75rem 1rem;
            cursor: pointer;
            transition: all 0.2s ease;
            font-size: 0.9rem;
            font-weight: 500;
        }}

        .topic-item:hover {{
            border-color: var(--primary);
            background: var(--bg-card-hover);
            transform: translateY(-2px);
        }}

        .topic-item.selected {{
            background: var(--gradient-1);
            border-color: transparent;
            color: white;
            box-shadow: 0 4px 15px var(--primary-glow);
        }}

        /* Buttons */
        .btn {{
            background: var(--gradient-1);
            border: none;
            border-radius: 10px;
            padding: 0.75rem 1.5rem;
            color: white;
            font-family: inherit;
            font-size: 0.95rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px var(--primary-glow);
        }}

        .btn:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }}

        .btn-secondary {{
            background: var(--bg-input);
            border: 1px solid var(--border);
        }}

        .btn-secondary:hover {{
            border-color: var(--primary);
            box-shadow: none;
        }}

        .btn-success {{
            background: var(--gradient-2);
        }}

        /* Paper Controls */
        .paper-controls {{
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1.5rem;
            flex-wrap: wrap;
        }}

        .mark-scheme-toggle {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            background: var(--bg-card);
            border: 1px solid var(--border);
            color: var(--text-soft);
            padding: 0.5rem 1rem;
            border-radius: 12px;
            font-family: 'Inter', sans-serif;
            font-size: 0.85rem;
            font-weight: 500;
            cursor: none !important;
            transition: all 0.3s ease;
        }}

        .mark-scheme-toggle:hover {{
            border-color: var(--success);
            color: var(--text);
        }}

        .toggle-switch {{
            position: relative;
            width: 44px;
            height: 24px;
            background: var(--bg-input);
            border-radius: 12px;
            transition: all 0.3s ease;
            border: 1px solid var(--border);
        }}

        .toggle-switch::after {{
            content: '';
            position: absolute;
            width: 18px;
            height: 18px;
            background: var(--text-soft);
            border-radius: 50%;
            top: 2px;
            left: 3px;
            transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        }}

        .mark-scheme-toggle.active .toggle-switch {{
            background: linear-gradient(135deg, var(--success) 0%, var(--teal) 100%);
            border-color: transparent;
        }}

        .mark-scheme-toggle.active .toggle-switch::after {{
            transform: translateX(20px);
            background: white;
        }}

        .mark-scheme-toggle.active {{
            color: var(--success);
            border-color: rgba(16, 185, 129, 0.3);
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(20, 184, 166, 0.08) 100%);
        }}

        .toggle-label {{
            font-weight: 500;
        }}

        .ai-process-btn {{
            position: relative;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            background: var(--gradient-1);
            border: none;
            color: white;
            padding: 0.6rem 1.2rem;
            border-radius: 10px;
            font-family: 'Inter', sans-serif;
            font-size: 0.85rem;
            font-weight: 500;
            letter-spacing: 0.02em;
            cursor: pointer;
            overflow: hidden;
            transition: all 0.3s ease;
        }}

        .ai-process-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px var(--primary-glow);
        }}

        .ai-process-btn .btn-glow {{
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            animation: shimmer 2s infinite;
        }}

        /* Large AI Process Button (below grid) */
        .ai-process-btn-large {{
            position: relative;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.75rem;
            background: var(--gradient-1);
            border: none;
            color: white;
            padding: 1rem 2.5rem;
            border-radius: 14px;
            font-family: 'Inter', sans-serif;
            font-size: 1.05rem;
            font-weight: 600;
            letter-spacing: 0.02em;
            cursor: pointer;
            overflow: hidden;
            transition: all 0.3s ease;
            box-shadow: 0 4px 20px var(--primary-glow);
        }}

        .ai-process-btn-large:hover {{
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 12px 35px var(--primary-glow);
        }}

        .ai-process-btn-large:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }}

        .ai-process-btn-large .btn-glow {{
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            animation: shimmer 2s infinite;
        }}

        .ai-process-btn-large .btn-icon {{
            font-size: 1.3rem;
        }}

        /* Modern section title */
        .section-title {{
            font-family: 'Inter', sans-serif;
            font-size: 0.95rem;
            font-weight: 600;
            letter-spacing: 0.01em;
            color: var(--text);
        }}

        /* Past Papers Grid Layout */
        .past-papers-grid {{
            display: grid;
            grid-template-columns: 100px repeat(3, 1fr);
            gap: 0.5rem;
            margin-top: 1rem;
        }}

        .pp-header {{
            background: var(--gradient-1);
            color: white;
            padding: 0.75rem;
            border-radius: 8px;
            text-align: center;
            font-weight: 600;
            font-size: 0.9rem;
        }}

        .pp-year {{
            background: var(--bg-input);
            border: 1px solid var(--border);
            padding: 0.6rem;
            border-radius: 8px;
            text-align: center;
            font-weight: 600;
            color: var(--text-soft);
        }}

        .pp-cell {{
            background: var(--bg-card);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            padding: 0.5rem;
            min-height: 60px;
            display: flex;
            flex-direction: column;
            gap: 0.3rem;
            transition: all 0.2s ease;
        }}

        .pp-cell:hover {{
            border-color: rgba(255, 255, 255, 0.1);
            background: var(--bg-card-hover);
        }}

        .pp-cell .paper-btn {{
            position: relative;
            background: var(--bg-input);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 8px;
            padding: 0.45rem 0.7rem;
            font-family: 'Inter', sans-serif;
            font-size: 0.75rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            color: var(--text-soft);
            text-align: left;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .pp-cell .paper-btn:hover {{
            background: var(--primary);
            border-color: var(--primary);
            color: white;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px var(--primary-glow);
        }}

        /* AI Mode Styling - Modern look */
        .pp-cell .paper-btn.ai-selectable {{
            border: 1px solid rgba(139, 92, 246, 0.25);
            background: rgba(139, 92, 246, 0.05);
        }}

        .pp-cell .paper-btn.ai-selectable:hover {{
            border-color: rgba(139, 92, 246, 0.5);
            background: rgba(139, 92, 246, 0.15);
        }}

        /* Modern selected state with animated checkmark */
        .pp-cell .paper-btn.ai-selected {{
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border: 1px solid transparent;
            color: white;
            box-shadow: 0 4px 15px var(--primary-glow);
            transform: scale(1.02);
        }}

        .pp-cell .paper-btn.ai-selected::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, transparent, rgba(255,255,255,0.1));
            border-radius: 7px;
        }}

        .pp-cell .paper-btn.ai-selected::after {{
            content: '✓';
            position: absolute;
            right: 6px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 0.7rem;
            font-weight: 700;
            animation: checkPop 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }}

        @keyframes checkPop {{
            0% {{ transform: translateY(-50%) scale(0); opacity: 0; }}
            50% {{ transform: translateY(-50%) scale(1.3); }}
            100% {{ transform: translateY(-50%) scale(1); opacity: 1; }}
        }}

        /* Ripple effect on click */
        .pp-cell .paper-btn.ripple {{
            overflow: hidden;
        }}

        .pp-cell .paper-btn .ripple-effect {{
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.4);
            transform: scale(0);
            animation: rippleAnim 0.6s ease-out;
            pointer-events: none;
        }}

        @keyframes rippleAnim {{
            to {{
                transform: scale(4);
                opacity: 0;
            }}
        }}

        /* Mark Scheme button styling */
        .pp-cell .paper-btn.ms-btn {{
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(20, 184, 166, 0.15) 100%);
            border: 1px solid rgba(16, 185, 129, 0.3);
            color: var(--success);
        }}

        .pp-cell .paper-btn.ms-btn:hover {{
            background: linear-gradient(135deg, var(--success) 0%, var(--teal) 100%);
            border-color: transparent;
            color: white;
            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
        }}

        .ms-icon {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: rgba(16, 185, 129, 0.2);
            padding: 0.15rem 0.35rem;
            border-radius: 4px;
            font-size: 0.65rem;
            font-weight: 600;
            letter-spacing: 0.03em;
            margin-right: 0.25rem;
        }}

        .pp-cell .paper-btn.ms-btn:hover .ms-icon {{
            background: rgba(255, 255, 255, 0.2);
        }}

        /* Results Section */
        .results-section {{
            margin-top: 2rem;
        }}

        .pdf-results {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 1rem;
        }}

        .pdf-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 1.25rem;
            transition: all 0.3s ease;
            transform-style: preserve-3d;
            perspective: 1000px;
        }}

        .pdf-card:hover {{
            border-color: var(--primary);
            transform: translateY(-8px) rotateX(3deg) rotateY(-2deg);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3), 0 0 20px var(--primary-glow);
        }}

        .pdf-card h4 {{
            font-size: 0.95rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: var(--text);
        }}

        .pdf-card .source {{
            color: var(--text-muted);
            font-size: 0.8rem;
            margin-bottom: 0.75rem;
        }}

        /* Page Grid */
        .page-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }}

        .page-item {{
            position: relative;
            cursor: pointer;
            border-radius: 10px;
            overflow: hidden;
            border: 3px solid transparent;
            transition: all 0.2s ease;
            background: var(--bg-card);
        }}

        .page-item:hover {{
            border-color: var(--primary);
            transform: scale(1.02);
        }}

        .page-item.selected {{
            border-color: var(--success);
            box-shadow: 0 0 20px var(--success-glow);
        }}

        .page-item img {{
            width: 100%;
            display: block;
        }}

        .page-number {{
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: linear-gradient(transparent, rgba(0,0,0,0.8));
            color: white;
            padding: 0.5rem 0.25rem 0.25rem;
            text-align: center;
            font-size: 0.8rem;
            font-weight: 500;
        }}

        .page-zoom-btn {{
            position: absolute;
            top: 6px;
            right: 6px;
            background: var(--primary);
            border: none;
            border-radius: 6px;
            padding: 4px 8px;
            color: white;
            font-size: 0.7rem;
            cursor: pointer;
            opacity: 0;
            transition: opacity 0.2s;
        }}

        .page-item:hover .page-zoom-btn {{
            opacity: 1;
        }}

        /* Collected Pages Panel */
        .collected-panel {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 1rem;
            margin-top: 1.5rem;
        }}

        .collected-panel h4 {{
            font-size: 0.95rem;
            font-weight: 600;
            margin-bottom: 0.75rem;
            color: var(--success);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .collected-thumbs {{
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
            max-height: 150px;
            overflow-y: auto;
        }}

        .collected-thumb {{
            position: relative;
            width: 60px;
            height: 80px;
            border-radius: 6px;
            overflow: hidden;
            border: 2px solid var(--success);
        }}

        .collected-thumb img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}

        .collected-thumb .remove-btn {{
            position: absolute;
            top: 2px;
            right: 2px;
            background: var(--danger);
            border: none;
            border-radius: 50%;
            width: 16px;
            height: 16px;
            color: white;
            font-size: 10px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        /* Status Bar */
        .status-bar {{
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: var(--bg-card);
            border-top: 1px solid var(--border);
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 100;
            backdrop-filter: blur(10px);
        }}

        .status-info {{
            display: flex;
            align-items: center;
            gap: 1.5rem;
        }}

        .status-badge {{
            background: var(--bg-input);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-size: 0.9rem;
        }}

        .status-badge.success {{
            border-color: var(--success);
            color: var(--success);
        }}

        .status-actions {{
            display: flex;
            gap: 0.75rem;
            align-items: center;
        }}

        /* Mark Schemes Checkbox */
        .ms-checkbox {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            background: var(--bg-input);
            border: 1px solid var(--border);
            border-radius: 8px;
            cursor: none;
            transition: all 0.2s ease;
        }}

        .ms-checkbox:hover {{
            border-color: var(--primary);
            background: rgba(139, 92, 246, 0.1);
        }}

        .ms-checkbox input[type="checkbox"] {{
            width: 18px;
            height: 18px;
            accent-color: var(--primary);
            cursor: none;
        }}

        .ms-checkbox-text {{
            font-size: 0.85rem;
            color: var(--text);
            font-weight: 500;
        }}

        /* Loading */
        .loading {{
            display: none;
            text-align: center;
            padding: 3rem;
        }}

        .loading.active {{
            display: block;
        }}

        .spinner {{
            width: 50px;
            height: 50px;
            border: 4px solid var(--border);
            border-top-color: var(--primary);
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
            margin: 0 auto 1rem;
        }}

        @keyframes spin {{
            to {{ transform: rotate(360deg); }}
        }}

        /* Enhanced Loading for AI Processing */
        .loading-progress {{
            max-width: 500px;
            margin: 1.5rem auto;
            padding: 1rem;
            background: var(--bg-input);
            border: 1px solid var(--border);
            border-radius: 12px;
            text-align: left;
        }}

        .loading-step {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.5rem 0;
            color: var(--text-soft);
            font-size: 0.9rem;
        }}

        .loading-step.active {{
            color: var(--primary);
        }}

        .loading-step.done {{
            color: var(--success);
        }}

        .loading-step-icon {{
            width: 24px;
            height: 24px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.75rem;
            background: var(--bg-input);
            border: 1px solid var(--border);
        }}

        .loading-step.active .loading-step-icon {{
            background: var(--primary);
            color: white;
            border-color: transparent;
            animation: pulse 1s infinite;
        }}

        .loading-step.done .loading-step-icon {{
            background: var(--success);
            color: white;
            border-color: transparent;
        }}

        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.1); }}
        }}

        /* AI Results Review Panel */
        .ai-results-panel {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1.5rem;
            margin-top: 1.5rem;
        }}

        .ai-results-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--border);
        }}

        .ai-results-title {{
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--text);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .ai-results-stats {{
            display: flex;
            gap: 1rem;
        }}

        .ai-stat {{
            padding: 0.4rem 0.8rem;
            background: var(--bg-input);
            border-radius: 8px;
            font-size: 0.85rem;
            color: var(--text-soft);
        }}

        .ai-stat strong {{
            color: var(--primary);
        }}

        .ai-papers-list {{
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }}

        .ai-paper-item {{
            background: var(--bg-input);
            border: 1px solid var(--border);
            border-radius: 12px;
            overflow: hidden;
        }}

        .ai-paper-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.75rem 1rem;
            background: rgba(139, 92, 246, 0.1);
            border-bottom: 1px solid var(--border);
        }}

        .ai-paper-title {{
            font-weight: 500;
            font-size: 0.9rem;
            color: var(--text);
        }}

        .ai-paper-pages-count {{
            font-size: 0.8rem;
            color: var(--primary);
            background: rgba(139, 92, 246, 0.2);
            padding: 0.25rem 0.6rem;
            border-radius: 12px;
        }}

        .ai-paper-pages {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
            gap: 1rem;
            padding: 1rem 1.25rem;
        }}

        .ai-page-thumb {{
            position: relative;
            aspect-ratio: 0.71;
            border-radius: 10px;
            overflow: hidden;
            cursor: none !important;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            background: var(--bg-card);
        }}

        .ai-page-thumb.high-confidence {{
            border: 3px solid var(--success);
            box-shadow: 0 0 15px rgba(16, 185, 129, 0.2);
        }}

        .ai-page-thumb.medium-confidence {{
            border: 3px solid var(--warning);
            box-shadow: 0 0 15px rgba(245, 158, 11, 0.2);
        }}

        .ai-page-thumb:hover {{
            transform: translateY(-5px) scale(1.02);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        }}

        .ai-page-thumb img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
        }}

        .ai-page-thumb .confidence-indicator {{
            position: absolute;
            top: 8px;
            left: 8px;
            padding: 0.3rem 0.6rem;
            border-radius: 6px;
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }}

        .ai-page-thumb .confidence-indicator.high {{
            background: var(--success);
            color: white;
        }}

        .ai-page-thumb .confidence-indicator.medium {{
            background: var(--warning);
            color: #1a1a1a;
        }}

        .ai-page-thumb .page-label {{
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: linear-gradient(transparent, rgba(0, 0, 0, 0.9));
            color: white;
            font-size: 0.85rem;
            font-weight: 500;
            padding: 1.5rem 0.5rem 0.5rem;
            text-align: center;
        }}

        .ai-page-thumb .remove-page {{
            position: absolute;
            top: 8px;
            right: 8px;
            width: 24px;
            height: 24px;
            background: rgba(239, 68, 68, 0.9);
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 0.85rem;
            cursor: none !important;
            display: none;
            align-items: center;
            justify-content: center;
            backdrop-filter: blur(5px);
        }}

        .ai-page-thumb:hover .remove-page {{
            display: flex;
        }}

        .ai-page-thumb .zoom-overlay {{
            position: absolute;
            inset: 0;
            background: rgba(139, 92, 246, 0.3);
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0;
            transition: opacity 0.2s ease;
        }}

        .ai-page-thumb:hover .zoom-overlay {{
            opacity: 1;
        }}

        .ai-page-thumb .zoom-icon {{
            width: 50px;
            height: 50px;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
            transform: scale(0.8);
            transition: transform 0.2s ease;
        }}

        .ai-page-thumb:hover .zoom-icon {{
            transform: scale(1);
        }}

        .ai-no-pages {{
            padding: 0.75rem 1rem;
            color: var(--text-soft);
            font-size: 0.85rem;
            font-style: italic;
        }}

        /* Success Animation */
        @keyframes successPop {{
            0% {{ transform: scale(0); opacity: 0; }}
            50% {{ transform: scale(1.2); }}
            100% {{ transform: scale(1); opacity: 1; }}
        }}

        @keyframes checkmarkDraw {{
            0% {{ stroke-dashoffset: 100; }}
            100% {{ stroke-dashoffset: 0; }}
        }}

        @keyframes confetti {{
            0% {{ transform: translateY(0) rotate(0deg); opacity: 1; }}
            100% {{ transform: translateY(-100px) rotate(720deg); opacity: 0; }}
        }}

        @keyframes successGlow {{
            0%, 100% {{ box-shadow: 0 0 20px var(--success-glow); }}
            50% {{ box-shadow: 0 0 40px var(--success-glow), 0 0 60px var(--success-glow); }}
        }}

        .success-modal {{
            position: fixed;
            inset: 0;
            background: rgba(0, 0, 0, 0.8);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
            backdrop-filter: blur(5px);
        }}

        .success-content {{
            background: var(--bg-card);
            border-radius: 24px;
            padding: 3rem;
            text-align: center;
            animation: successPop 0.5s ease-out;
            border: 2px solid var(--success);
            box-shadow: 0 0 30px var(--success-glow);
            animation: successPop 0.5s ease-out, successGlow 2s ease-in-out infinite;
            position: relative;
            overflow: hidden;
        }}

        .success-checkmark {{
            width: 80px;
            height: 80px;
            margin: 0 auto 1.5rem;
            background: var(--gradient-2);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            animation: successPop 0.6s ease-out;
        }}

        .success-checkmark svg {{
            width: 40px;
            height: 40px;
            stroke: white;
            stroke-width: 3;
            fill: none;
            stroke-linecap: round;
            stroke-linejoin: round;
        }}

        .success-checkmark svg path {{
            stroke-dasharray: 100;
            animation: checkmarkDraw 0.8s ease-out forwards;
            animation-delay: 0.3s;
        }}

        .success-title {{
            font-size: 1.8rem;
            font-weight: 700;
            color: var(--text);
            margin-bottom: 0.5rem;
        }}

        .success-message {{
            color: var(--text-soft);
            font-size: 1rem;
            margin-bottom: 1.5rem;
        }}

        .confetti-piece {{
            position: absolute;
            width: 10px;
            height: 10px;
            border-radius: 2px;
            animation: confetti 1.5s ease-out forwards;
        }}

        .hidden {{ display: none !important; }}

        /* Zoom Modal */
        .zoom-modal {{
            position: fixed;
            inset: 0;
            background: rgba(0, 0, 0, 0.95);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            cursor: zoom-out;
        }}

        .zoom-modal img {{
            max-width: 90vw;
            max-height: 90vh;
            border-radius: 8px;
        }}

        /* Info Boxes */
        .info-box {{
            border-radius: 10px;
            padding: 0.85rem 1.25rem;
            margin-bottom: 1rem;
            font-size: 0.9rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}

        .info-box.success {{
            background: var(--success-glow);
            border: 1px solid var(--success);
            color: var(--success);
        }}

        .info-box.warning {{
            background: rgba(245, 158, 11, 0.15);
            border: 1px solid var(--warning);
            color: var(--warning);
        }}

        /* Main Tab Navigation */
        .main-tabs {{
            display: flex;
            gap: 0.5rem;
            margin-bottom: 1.5rem;
            background: var(--bg-card);
            padding: 0.4rem;
            border-radius: 14px;
            border: 1px solid var(--border);
        }}

        .main-tab {{
            flex: 1;
            padding: 0.85rem 1.5rem;
            border: none;
            background: transparent;
            color: var(--text-soft);
            font-family: 'Inter', sans-serif;
            font-size: 0.95rem;
            font-weight: 500;
            border-radius: 10px;
            cursor: none !important;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.6rem;
        }}

        .main-tab:hover {{
            color: var(--text);
            background: var(--bg-input);
        }}

        .main-tab.active {{
            background: var(--gradient-1);
            color: white;
            box-shadow: 0 4px 15px var(--primary-glow);
        }}

        .main-tab-icon {{
            font-size: 1.1rem;
        }}

        /* Custom Resources Section */
        .custom-resources-section {{
            display: none;
        }}

        .custom-resources-section.active {{
            display: block;
        }}

        .upload-zone {{
            border: 2px dashed var(--border);
            border-radius: 16px;
            padding: 3rem 2rem;
            text-align: center;
            background: var(--bg-card);
            transition: all 0.3s ease;
            margin-bottom: 1.5rem;
        }}

        .upload-zone:hover, .upload-zone.drag-over {{
            border-color: var(--primary);
            background: rgba(139, 92, 246, 0.05);
        }}

        .upload-zone.drag-over {{
            transform: scale(1.01);
            box-shadow: 0 0 30px var(--primary-glow);
        }}

        .upload-icon {{
            font-size: 3rem;
            margin-bottom: 1rem;
            display: block;
        }}

        .upload-text {{
            color: var(--text);
            font-size: 1.1rem;
            font-weight: 500;
            margin-bottom: 0.5rem;
        }}

        .upload-subtext {{
            color: var(--text-soft);
            font-size: 0.9rem;
        }}

        .upload-btn {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: var(--gradient-1);
            color: white;
            padding: 0.75rem 1.5rem;
            border-radius: 10px;
            border: none;
            font-family: 'Inter', sans-serif;
            font-size: 0.95rem;
            font-weight: 500;
            cursor: none !important;
            margin-top: 1rem;
            transition: all 0.3s ease;
        }}

        .upload-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px var(--primary-glow);
        }}

        /* Uploaded PDF info */
        .uploaded-pdf-info {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.25rem;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 1rem;
        }}

        .uploaded-pdf-icon {{
            font-size: 2.5rem;
        }}

        .uploaded-pdf-details {{
            flex: 1;
        }}

        .uploaded-pdf-name {{
            font-weight: 600;
            color: var(--text);
            margin-bottom: 0.25rem;
        }}

        .uploaded-pdf-meta {{
            color: var(--text-soft);
            font-size: 0.85rem;
        }}

        .uploaded-pdf-remove {{
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.3);
            color: #ef4444;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            font-size: 0.85rem;
            cursor: none !important;
            transition: all 0.3s ease;
        }}

        .uploaded-pdf-remove:hover {{
            background: #ef4444;
            color: white;
        }}

        /* Topic selection for custom resources */
        .custom-topic-section {{
            margin-bottom: 1.5rem;
        }}

        .custom-topic-section label {{
            display: block;
            margin-bottom: 0.75rem;
            font-weight: 500;
            color: var(--text);
        }}

        /* Scan button */
        .scan-btn {{
            width: 100%;
            padding: 1rem 2rem;
            background: var(--gradient-2);
            border: none;
            color: white;
            font-family: 'Inter', sans-serif;
            font-size: 1rem;
            font-weight: 600;
            border-radius: 12px;
            cursor: none !important;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.75rem;
        }}

        .scan-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(16, 185, 129, 0.3);
        }}

        .scan-btn:disabled {{
            opacity: 0.5;
            cursor: not-allowed !important;
            transform: none;
        }}

        /* Custom results - page cards with confidence */
        .custom-results-section {{
            margin-top: 1.5rem;
        }}

        .confidence-legend {{
            display: flex;
            gap: 1.5rem;
            margin-bottom: 1rem;
            padding: 1rem;
            background: var(--bg-card);
            border-radius: 10px;
            border: 1px solid var(--border);
        }}

        .legend-item {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.85rem;
            color: var(--text-soft);
        }}

        .legend-dot {{
            width: 12px;
            height: 12px;
            border-radius: 50%;
        }}

        .legend-dot.high {{
            background: var(--success);
            box-shadow: 0 0 8px rgba(16, 185, 129, 0.5);
        }}

        .legend-dot.medium {{
            background: var(--warning);
            box-shadow: 0 0 8px rgba(245, 158, 11, 0.5);
        }}

        /* Page cards with confidence borders */
        .custom-page-card {{
            position: relative;
            border-radius: 12px;
            overflow: hidden;
            transition: all 0.3s ease;
            cursor: none !important;
        }}

        .custom-page-card.high-confidence {{
            border: 3px solid var(--success);
            box-shadow: 0 0 15px rgba(16, 185, 129, 0.3);
        }}

        .custom-page-card.medium-confidence {{
            border: 3px solid var(--warning);
            box-shadow: 0 0 15px rgba(245, 158, 11, 0.3);
        }}

        .custom-page-card:hover {{
            transform: translateY(-3px);
        }}

        .custom-page-card.high-confidence:hover {{
            box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4);
        }}

        .custom-page-card.medium-confidence:hover {{
            box-shadow: 0 8px 25px rgba(245, 158, 11, 0.4);
        }}

        .custom-page-card.selected {{
            transform: scale(1.02);
        }}

        .custom-page-card.selected.high-confidence {{
            box-shadow: 0 0 25px rgba(16, 185, 129, 0.5);
        }}

        .custom-page-card.selected.medium-confidence {{
            box-shadow: 0 0 25px rgba(245, 158, 11, 0.5);
        }}

        .confidence-badge {{
            position: absolute;
            top: 8px;
            right: 8px;
            padding: 0.3rem 0.6rem;
            border-radius: 6px;
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }}

        .confidence-badge.high {{
            background: var(--success);
            color: white;
        }}

        .confidence-badge.medium {{
            background: var(--warning);
            color: #1a1a2e;
        }}

        .page-number-badge {{
            position: absolute;
            bottom: 8px;
            left: 8px;
            background: rgba(0, 0, 0, 0.7);
            color: white;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 500;
        }}

        .custom-page-thumb {{
            width: 100%;
            aspect-ratio: 1 / 1.4;
            object-fit: cover;
            display: block;
        }}

        /* Selection overlay for custom pages */
        .custom-page-card .select-overlay {{
            position: absolute;
            inset: 0;
            background: transparent;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
        }}

        .custom-page-card.selected .select-overlay {{
            background: rgba(139, 92, 246, 0.3);
        }}

        .custom-page-card .select-check {{
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: var(--primary);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1rem;
            opacity: 0;
            transform: scale(0.5);
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }}

        .custom-page-card.selected .select-check {{
            opacity: 1;
            transform: scale(1);
        }}

        .zoom-btn-custom {{
            position: absolute;
            bottom: 30px;
            right: 6px;
            width: 28px;
            height: 28px;
            background: rgba(59, 130, 246, 0.9);
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 0.85rem;
            cursor: none !important;
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0;
            transition: all 0.2s ease;
            z-index: 5;
        }}

        .custom-page-card:hover .zoom-btn-custom {{
            opacity: 1;
        }}

        .zoom-btn-custom:hover {{
            background: rgba(59, 130, 246, 1);
            transform: scale(1.1);
        }}

        /* Scanning animation */
        .scanning-overlay {{
            position: fixed;
            inset: 0;
            background: rgba(0, 0, 0, 0.8);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 9999;
        }}

        .scanning-animation {{
            width: 120px;
            height: 120px;
            position: relative;
            margin-bottom: 1.5rem;
        }}

        .scanning-circle {{
            position: absolute;
            inset: 0;
            border: 3px solid transparent;
            border-top-color: var(--primary);
            border-radius: 50%;
            animation: scan-spin 1s linear infinite;
        }}

        .scanning-circle:nth-child(2) {{
            inset: 10px;
            border-top-color: var(--secondary);
            animation-duration: 1.5s;
            animation-direction: reverse;
        }}

        .scanning-circle:nth-child(3) {{
            inset: 20px;
            border-top-color: var(--success);
            animation-duration: 2s;
        }}

        .scanning-icon {{
            position: absolute;
            inset: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
        }}

        @keyframes scan-spin {{
            to {{ transform: rotate(360deg); }}
        }}

        .scanning-text {{
            color: white;
            font-size: 1.1rem;
            font-weight: 500;
        }}

        .scanning-subtext {{
            color: var(--text-soft);
            font-size: 0.9rem;
            margin-top: 0.5rem;
        }}

        /* Responsive */
        @media (max-width: 768px) {{
            .form-row {{
                grid-template-columns: 1fr;
            }}
            .past-papers-grid {{
                grid-template-columns: 80px repeat(3, 1fr);
            }}
            header h1 {{
                font-size: 2rem;
            }}
        }}
    </style>
</head>
<body>
    <!-- Theme Switcher -->
    <div class="theme-switcher">
        <button class="theme-btn active" onclick="setTheme('default')" id="theme-default">🌙 Dark</button>
        <button class="theme-btn" onclick="setTheme('intuitive')" id="theme-intuitive">💎 Intuitive</button>
    </div>

    <div class="bg-effects">
        <div class="bg-orb bg-orb-1"></div>
        <div class="bg-orb bg-orb-2"></div>
        <div class="bg-orb bg-orb-3"></div>
    </div>

    <!-- Custom Cursor System -->
    <div class="cursor-dot" id="cursorDot"></div>
    <div class="cursor-ring" id="cursorRing"></div>
    <div class="cursor-glow" id="cursorGlow"></div>

    <div class="container">
        <header>
            <h1>🔥 MathsForge AI</h1>
            <p>AI-powered worksheet generation from past papers & resources</p>
        </header>

        <!-- Main Tab Navigation -->
        <div class="main-tabs">
            <button class="main-tab active" id="tabPastPapers" onclick="switchMainTab('pastpapers')">
                <span class="main-tab-icon">📚</span>
                <span>Past Papers</span>
            </button>
            <button class="main-tab" id="tabCustomResources" onclick="switchMainTab('custom')">
                <span class="main-tab-icon">📁</span>
                <span>Custom Resources</span>
            </button>
        </div>

        <!-- PAST PAPERS TAB CONTENT -->
        <div class="past-papers-tab-content" id="pastPapersContent">

        <!-- AI-Enhanced Mode Toggle - Prominent Position -->
        <div class="ai-mode-banner" id="aiModeBanner">
            <div class="ai-mode-content">
                <div class="ai-mode-left">
                    <span class="ai-badge">🤖 NEW</span>
                    <div class="ai-mode-info">
                        <h3>AI-Enhanced Mode</h3>
                        <p>Automatically detect topic questions from multiple past papers</p>
                    </div>
                </div>
                <button class="ai-toggle-btn" id="aiToggleBtn" onclick="toggleAIModeGlobal()">
                    <span class="toggle-track">
                        <span class="toggle-thumb"></span>
                    </span>
                    <span class="toggle-label">Enable</span>
                </button>
            </div>
            <div class="ai-disclaimer hidden" id="aiDisclaimer">
                <span>⚠️ AI can make mistakes. Please double-check your PDF before confirming.</span>
            </div>
        </div>

        <div class="search-section animate-fade-in">
            <div class="form-row">
                <div class="form-group">
                    <label>📚 Level</label>
                    <div class="custom-select" id="levelSelect">
                        <div class="custom-select-trigger" onclick="toggleCustomSelect('levelSelect')">
                            <span class="custom-select-value" data-value="gcse">GCSE</span>
                            <span class="custom-select-arrow">▼</span>
                        </div>
                        <div class="custom-select-options">
                            <div class="custom-select-option selected" data-value="gcse" onclick="selectOption('levelSelect', 'gcse', 'GCSE')">GCSE</div>
                            <div class="custom-select-option" data-value="ks3" onclick="selectOption('levelSelect', 'ks3', 'KS3 (Year 7-9)')">KS3 (Year 7-9)</div>
                        </div>
                    </div>
                    <input type="hidden" id="level" value="gcse">
                </div>
                <div class="form-group">
                    <label>🎯 Difficulty</label>
                    <div class="custom-select" id="difficultySelect">
                        <div class="custom-select-trigger" onclick="toggleCustomSelect('difficultySelect')">
                            <span class="custom-select-value" data-value="pastpapers">Past Papers Only</span>
                            <span class="custom-select-arrow">▼</span>
                        </div>
                        <div class="custom-select-options">
                            <div class="custom-select-option" data-value="medium" onclick="selectOption('difficultySelect', 'medium', 'Medium')">Medium</div>
                            <div class="custom-select-option" data-value="hard" onclick="selectOption('difficultySelect', 'hard', 'Hard')">Hard</div>
                            <div class="custom-select-option" data-value="harder" onclick="selectOption('difficultySelect', 'harder', 'Harder (Grade 8-9)')">Harder (Grade 8-9)</div>
                            <div class="custom-select-option selected" data-value="pastpapers" onclick="selectOption('difficultySelect', 'pastpapers', 'Past Papers Only')">Past Papers Only</div>
                        </div>
                    </div>
                    <input type="hidden" id="difficulty" value="pastpapers">
                </div>
                <div class="form-group" id="keywordsGroup">
                    <label>🔍 Keywords (optional)</label>
                    <input type="text" id="keywords" placeholder="Auto-filtered by topic">
                </div>
            </div>

            <label>📋 Choose a Topic</label>
            <div class="topic-grid" id="topicGrid"></div>
        </div>

        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p id="loadingText">Searching for PDFs...</p>
        </div>

        <!-- AI Results Review Panel -->
        <div class="ai-results-panel hidden" id="aiResultsPanel">
            <div class="ai-results-header">
                <div class="ai-results-title">
                    <span>🤖</span>
                    <span>AI Found Pages for "<span id="aiResultsTopic"></span>"</span>
                </div>
                <div class="ai-results-stats">
                    <div class="ai-stat"><strong id="aiTotalPages">0</strong> pages</div>
                    <div class="ai-stat"><strong id="aiTotalPapers">0</strong> papers</div>
                </div>
            </div>
            <div class="ai-papers-list" id="aiPapersList"></div>
        </div>

        <div class="results-section hidden" id="resultsSection">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <h3 class="section-title">📄 Found PDFs</h3>
                <button class="btn btn-secondary" onclick="startOver()" style="padding: 0.5rem 1rem; font-size: 0.85rem; font-family: 'Inter', sans-serif; font-weight: 500;">↻ New Search</button>
            </div>
            <div id="pastPapersContainer"></div>
            <div class="pdf-results" id="pdfResults"></div>

            <!-- Loading Progress Steps (shown during AI processing) -->
            <div class="loading-progress hidden" id="loadingProgress">
                <div class="loading-step" id="loadingStep1">
                    <div class="loading-step-icon">1</div>
                    <span>Downloading papers...</span>
                </div>
                <div class="loading-step" id="loadingStep2">
                    <div class="loading-step-icon">2</div>
                    <span>Generating thumbnails...</span>
                </div>
                <div class="loading-step" id="loadingStep3">
                    <div class="loading-step-icon">3</div>
                    <span>Scanning for topic keywords...</span>
                </div>
                <div class="loading-step" id="loadingStep4">
                    <div class="loading-step-icon">4</div>
                    <span>Preparing results...</span>
                </div>
            </div>

            <div id="pageSection" class="hidden" style="margin-top: 2rem;">
                <h3 style="margin-bottom: 1rem; font-weight: 700;">✅ Select Pages</h3>
                <div class="page-grid" id="pageGrid"></div>
            </div>

            <!-- Collected Pages Panel -->
            <div class="collected-panel hidden" id="collectedPanel">
                <h4>📦 Collected Pages</h4>
                <div class="collected-thumbs" id="collectedThumbs"></div>
            </div>
        </div>
        </div><!-- END Past Papers Tab Content -->

        <!-- CUSTOM RESOURCES TAB CONTENT -->
        <div class="custom-resources-section" id="customResourcesContent">
            <div class="search-section animate-fade-in">
                <!-- Upload Zone -->
                <div class="upload-zone" id="uploadZone">
                    <span class="upload-icon">📄</span>
                    <p class="upload-text">Drag & drop your PDF here</p>
                    <p class="upload-subtext">or click to browse (textbooks, worksheets, revision guides)</p>
                    <button class="upload-btn" onclick="document.getElementById('customPdfInput').click()">
                        <span>📁</span> Choose File
                    </button>
                    <input type="file" id="customPdfInput" accept=".pdf" style="display: none;" onchange="handleCustomPdfUpload(event)">
                </div>

                <!-- Uploaded PDF Info (hidden by default) -->
                <div class="uploaded-pdf-info hidden" id="uploadedPdfInfo">
                    <span class="uploaded-pdf-icon">📕</span>
                    <div class="uploaded-pdf-details">
                        <div class="uploaded-pdf-name" id="uploadedPdfName">document.pdf</div>
                        <div class="uploaded-pdf-meta" id="uploadedPdfMeta">0 pages • 0 MB</div>
                    </div>
                    <button class="uploaded-pdf-remove" onclick="removeUploadedPdf()">✕ Remove</button>
                </div>

                <!-- Topic Selection for Custom Resources -->
                <div class="custom-topic-section hidden" id="customTopicSection">
                    <label>🎯 Select Topic to Filter</label>
                    <div class="topic-grid" id="customTopicGrid"></div>
                </div>

                <!-- Scan Button -->
                <button class="scan-btn hidden" id="scanBtn" onclick="scanCustomPdf()" disabled>
                    <span>🔍</span>
                    <span>Scan PDF for Topic</span>
                </button>
            </div>

            <!-- Custom Results Section -->
            <div class="custom-results-section hidden" id="customResultsSection">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <h3 class="section-title">📄 Relevant Pages Found</h3>
                    <button class="btn btn-secondary" onclick="resetCustomResources()" style="padding: 0.5rem 1rem; font-size: 0.85rem;">↻ Start Over</button>
                </div>

                <!-- Confidence Legend -->
                <div class="confidence-legend">
                    <div class="legend-item">
                        <div class="legend-dot high"></div>
                        <span><strong>Definitely</strong> related - auto-selected</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-dot medium"></div>
                        <span><strong>Maybe</strong> related - review recommended</span>
                    </div>
                </div>

                <!-- Results Stats -->
                <div class="info-box success" id="customResultsStats">
                    <span>✅</span>
                    <span id="customResultsText">Found 0 relevant pages</span>
                </div>

                <!-- Page Grid -->
                <div class="page-grid" id="customPageGrid"></div>
            </div>
        </div><!-- END Custom Resources Tab Content -->
    </div>

    <div class="status-bar hidden" id="statusBar">
        <div class="status-info">
            <span class="status-badge"><span id="selectedCount">0</span> pages selected</span>
            <span class="status-badge success hidden" id="collectedBadge">📦 <span id="collectedCount">0</span> collected</span>
        </div>
        <div class="status-actions">
            <button class="btn btn-secondary" onclick="startOver()">Start Over</button>
            <button class="btn btn-secondary hidden" id="addMoreBtn" onclick="addMorePDFs()">+ Add More</button>
            <button class="btn" id="confirmBtn" onclick="confirmSelection()">✓ Confirm</button>
            <button class="btn btn-secondary hidden" id="editBtn" onclick="editSelection()">↩️ Deselect</button>
            <label class="ms-checkbox hidden" id="msCheckboxLabel">
                <input type="checkbox" id="includeMarkSchemes" checked>
                <span class="ms-checkbox-text">📝 Include Mark Schemes</span>
            </label>
            <button class="btn btn-success hidden" id="generateBtn" onclick="generatePDF()">📥 Generate PDF</button>
        </div>
    </div>

    <div class="zoom-modal hidden" id="zoomModal" onclick="closeZoom()">
        <img id="zoomImage" src="">
    </div>

    <!-- Success Animation Modal -->
    <div class="success-modal hidden" id="successModal" onclick="closeSuccessModal()">
        <div class="success-content" onclick="event.stopPropagation()">
            <div class="success-checkmark">
                <svg viewBox="0 0 24 24">
                    <path d="M5 13l4 4L19 7"/>
                </svg>
            </div>
            <h2 class="success-title">PDF Generated!</h2>
            <p class="success-message" id="successMessage">Your homework worksheet is ready</p>
            <button class="btn btn-success" onclick="closeSuccessModal()">Done</button>
        </div>
    </div>

    <script>
        const TOPICS = {topics_json};

        let selectedTopic = null;
        let selectedPages = new Set();
        let currentPDF = null;
        let currentPDFTitle = '';
        let selectionConfirmed = false;

        // Multi-PDF support - PERSISTENT across PDF loads
        let collectedPages = [];  // Array of {{pdfPath, pages: [1,2,3], title, thumbnails}}
        let loadedPDFs = [];      // Track all loaded PDFs

        // Populate topics
        const topicGrid = document.getElementById('topicGrid');
        TOPICS.forEach(topic => {{
            const div = document.createElement('div');
            div.className = 'topic-item';
            div.textContent = topic;
            div.onclick = () => selectTopic(topic, div);
            topicGrid.appendChild(div);
        }});

        // Difficulty change handler
        document.getElementById('difficulty').addEventListener('change', function() {{
            const keywordsGroup = document.getElementById('keywordsGroup');
            const keywordsInput = document.getElementById('keywords');
            const level = document.getElementById('level').value;

            // KS3 should never have pastpapers option
            if (level === 'ks3' && this.value === 'pastpapers') {{
                this.value = 'medium';
                alert('Past Papers mode is only available for GCSE level.');
                return;
            }}

            if (this.value === 'pastpapers') {{
                keywordsGroup.style.opacity = '0.5';
                keywordsInput.disabled = true;
                keywordsInput.placeholder = 'Auto-filtered by topic';
            }} else {{
                keywordsGroup.style.opacity = '1';
                keywordsInput.disabled = false;
                keywordsInput.placeholder = 'e.g., tree diagram, conditional';
            }}
            if (selectedTopic) {{
                // DON'T reset collected pages when changing difficulty!
                selectedPages.clear();
                currentPDF = null;
                selectionConfirmed = false;
                document.getElementById('pageSection').classList.add('hidden');
                searchPDFs();
            }}
        }});

        // Level change handler
        document.getElementById('level').addEventListener('change', function() {{
            const difficultySelect = document.getElementById('difficulty');
            const pastPapersOption = difficultySelect.querySelector('option[value="pastpapers"]');

            // Show/hide Past Papers option based on level
            if (this.value === 'ks3') {{
                // Hide Past Papers for KS3
                if (pastPapersOption) {{
                    pastPapersOption.style.display = 'none';
                    // If currently on pastpapers, switch to medium
                    if (difficultySelect.value === 'pastpapers') {{
                        difficultySelect.value = 'medium';
                    }}
                }}
            }} else {{
                // Show Past Papers for GCSE
                if (pastPapersOption) {{
                    pastPapersOption.style.display = '';
                }}
            }}

            if (selectedTopic) {{
                selectedPages.clear();
                currentPDF = null;
                selectionConfirmed = false;
                document.getElementById('pageSection').classList.add('hidden');
                searchPDFs();
            }}
        }});

        function selectTopic(topic, element) {{
            document.querySelectorAll('.topic-item').forEach(el => el.classList.remove('selected'));
            element.classList.add('selected');
            selectedTopic = topic;

            // Hide page section when switching topics (but keep collected pages)
            selectedPages.clear();
            currentPDF = null;
            selectionConfirmed = false;
            document.getElementById('pageSection').classList.add('hidden');

            // Update button states but keep collected pages visible
            document.getElementById('confirmBtn').classList.remove('hidden');
            document.getElementById('editBtn').classList.add('hidden');
            document.getElementById('generateBtn').classList.add('hidden');
            document.getElementById('addMoreBtn').classList.add('hidden');

            // Update selected count to 0
            updateSelectedCount();

            searchPDFs();
        }}

        async function searchPDFs() {{
            const level = document.getElementById('level').value;
            const difficulty = document.getElementById('difficulty').value;
            const keywords = document.getElementById('keywords').value;

            document.getElementById('loading').classList.add('active');
            document.getElementById('resultsSection').classList.add('hidden');

            try {{
                const response = await fetch('/api/search', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        topic: selectedTopic,
                        level: level,
                        difficulty: difficulty,
                        keywords: keywords
                    }})
                }});

                const data = await response.json();
                displayResults(data.results);
            }} catch (error) {{
                console.error('Search error:', error);
                alert('Error searching for PDFs');
            }}

            document.getElementById('loading').classList.remove('active');
        }}

        function displayResults(results) {{
            const container = document.getElementById('pdfResults');
            const ppContainer = document.getElementById('pastPapersContainer');
            container.innerHTML = '';
            ppContainer.innerHTML = '';

            if (results.length === 0) {{
                container.innerHTML = '<p style="color: var(--text-muted); padding: 2rem; text-align: center;">No PDFs found. Try different keywords or topic.</p>';
                document.getElementById('resultsSection').classList.remove('hidden');
                return;
            }}

            const difficulty = document.getElementById('difficulty').value;

            if (difficulty === 'pastpapers') {{
                // Create grid layout for past papers (years as rows, papers as columns)
                // Specimen at bottom as requested
                const years = ['2024', '2023', '2022', '2021', '2020', '2019', '2018', '2017', 'Specimen'];
                const papers = ['Paper 1', 'Paper 2', 'Paper 3'];

                // Organize results by year, paper, and type (QP vs MS)
                const organized = {{}};
                results.forEach((pdf, index) => {{
                    const year = pdf.year || 'Unknown';
                    const paper = pdf.paper || 'Paper';
                    const isMS = pdf.is_mark_scheme || pdf.title.includes(' MS') || pdf.title.toLowerCase().includes('mark');
                    const type = isMS ? 'ms' : 'qp';

                    if (!organized[year]) organized[year] = {{}};
                    if (!organized[year][paper]) organized[year][paper] = {{qp: [], ms: []}};
                    organized[year][paper][type].push({{...pdf, index}});
                }});

                let html = `
                    <div class="paper-controls">
                        <button class="mark-scheme-toggle" id="markSchemeToggle" onclick="toggleMarkSchemesBtn()">
                            <div class="toggle-switch"></div>
                            <span class="toggle-label">Mark Schemes</span>
                        </button>
                    </div>
                `;

                html += '<div class="past-papers-grid">';
                // Header row
                html += '<div class="pp-header">Year</div>';
                papers.forEach(p => {{
                    html += `<div class="pp-header">${{p}}</div>`;
                }});

                // Data rows
                years.forEach(year => {{
                    html += `<div class="pp-year">${{year}}</div>`;
                    papers.forEach(paper => {{
                        html += '<div class="pp-cell">';
                        if (organized[year] && organized[year][paper]) {{
                            // Question papers
                            organized[year][paper].qp.forEach(pdf => {{
                                const sessionLabel = pdf.session !== 'Unknown' ? pdf.session.substring(0, 3) : '';
                                html += `<button class="paper-btn qp-btn ripple" onclick="handlePaperClick(${{pdf.index}}, this, event)" title="${{pdf.title}}">📄 ${{sessionLabel || 'QP'}}</button>`;
                            }});
                            // Mark schemes (hidden by default)
                            organized[year][paper].ms.forEach(pdf => {{
                                const sessionLabel = pdf.session !== 'Unknown' ? pdf.session.substring(0, 3) : '';
                                html += `<button class="paper-btn ms-btn" style="display: none;" onclick="loadPDF(${{pdf.index}})" title="${{pdf.title}}"><span class="ms-icon">MS</span> ${{sessionLabel}}</button>`;
                            }});
                        }}
                        html += '</div>';
                    }});
                }});

                // Add Unknown/Other at the end if there are any
                if (organized['Unknown']) {{
                    html += '<div class="pp-year">Other</div>';
                    papers.forEach(paper => {{
                        html += '<div class="pp-cell">';
                        if (organized['Unknown'] && organized['Unknown'][paper]) {{
                            organized['Unknown'][paper].qp.forEach(pdf => {{
                                html += `<button class="paper-btn qp-btn" onclick="loadPDF(${{pdf.index}})">📄 QP</button>`;
                            }});
                            organized['Unknown'][paper].ms.forEach(pdf => {{
                                html += `<button class="paper-btn ms-btn" style="display: none;" onclick="loadPDF(${{pdf.index}})"><span class="ms-icon">MS</span></button>`;
                            }});
                        }}
                        html += '</div>';
                    }});
                }}

                html += '</div>';

                // Add AI Process button below the grid (bigger, more prominent)
                html += `
                    <div class="ai-process-container" style="margin-top: 1.5rem; text-align: center;">
                        <button id="aiProcessBtn" class="ai-process-btn-large" style="display: none;" onclick="processAIPapers()">
                            <span class="btn-glow"></span>
                            <span class="btn-icon">🤖</span>
                            <span>Process Selected Papers (<span id="selectedPaperCount">0</span>)</span>
                        </button>
                    </div>
                `;

                ppContainer.innerHTML = html;
            }} else {{
                // Standard display for other modes
                results.forEach((pdf, index) => {{
                    const card = document.createElement('div');
                    card.className = 'pdf-card';
                    card.innerHTML = `
                        <h4>${{pdf.title}}</h4>
                        <p class="source">${{pdf.source}}</p>
                        <button class="btn" style="margin-top: 0.75rem; padding: 0.6rem 1.25rem; font-size: 0.9rem;" onclick="loadPDF(${{index}})">📄 Load PDF</button>
                    `;
                    container.appendChild(card);
                }});
            }}

            document.getElementById('resultsSection').classList.remove('hidden');
            window.pdfResults = results;

            // Show AI Process button if AI mode is enabled
            const aiProcessBtn = document.getElementById('aiProcessBtn');
            if (aiProcessBtn && aiModeEnabled) {{
                aiProcessBtn.style.display = '';
                document.querySelectorAll('.qp-btn').forEach(btn => {{
                    btn.classList.add('ai-selectable');
                }});
                selectedPapersForAI.clear();
                updateAIProcessButton();
            }}

            // Show status bar if we have collected pages
            if (collectedPages.length > 0) {{
                document.getElementById('statusBar').classList.remove('hidden');
                updateCollectedDisplay();
            }}
        }}

        function handlePaperClick(index, btn, event) {{
            // Add ripple effect
            createRipple(event, btn);

            // If AI mode is enabled, toggle selection instead of loading
            if (aiModeEnabled) {{
                togglePaperForAI(index, btn);
            }} else {{
                loadPDF(index);
            }}
        }}

        function createRipple(event, element) {{
            const ripple = document.createElement('span');
            ripple.className = 'ripple-effect';
            const rect = element.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = (event.clientX - rect.left - size / 2) + 'px';
            ripple.style.top = (event.clientY - rect.top - size / 2) + 'px';
            element.appendChild(ripple);
            setTimeout(() => ripple.remove(), 600);
        }}

        async function loadPDF(index) {{
            const pdf = window.pdfResults[index];
            currentPDFTitle = pdf.title;
            document.getElementById('loadingText').textContent = 'Loading PDF pages...';
            document.getElementById('loading').classList.add('active');

            try {{
                const response = await fetch('/api/load-pdf', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ url: pdf.url, topic: selectedTopic }})
                }});

                const data = await response.json();
                if (data.error) {{
                    alert('Error loading PDF: ' + data.error);
                    document.getElementById('loading').classList.remove('active');
                    return;
                }}

                currentPDF = data.path;

                // Track loaded PDF
                loadedPDFs.push({{
                    path: data.path,
                    url: pdf.url,
                    title: pdf.title,
                    thumbnails: data.thumbnails
                }});

                displayPages(data.thumbnails, data.filtered_pages);

                setTimeout(() => {{
                    document.getElementById('pageSection').scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                }}, 100);

            }} catch (error) {{
                console.error('Load error:', error);
                alert('Error loading PDF');
            }}

            document.getElementById('loading').classList.remove('active');
        }}

        function displayPages(thumbnails, filteredPages) {{
            const container = document.getElementById('pageGrid');
            container.innerHTML = '';
            selectedPages.clear();
            selectionConfirmed = false;

            // Update buttons for new PDF
            document.getElementById('confirmBtn').classList.remove('hidden');
            document.getElementById('editBtn').classList.add('hidden');
            document.getElementById('generateBtn').classList.add('hidden');
            document.getElementById('addMoreBtn').classList.add('hidden');

            // Pre-select filtered pages
            if (filteredPages && filteredPages.length > 0) {{
                filteredPages.forEach(p => selectedPages.add(p + 1));
                const infoDiv = document.createElement('div');
                infoDiv.className = 'info-box success';
                infoDiv.style.gridColumn = '1/-1';
                infoDiv.innerHTML = `✓ Auto-selected ${{filteredPages.length}} pages containing topic keywords. Click pages to add/remove.`;
                container.appendChild(infoDiv);
            }} else if (document.getElementById('difficulty').value === 'pastpapers') {{
                const warnDiv = document.createElement('div');
                warnDiv.className = 'info-box warning';
                warnDiv.style.gridColumn = '1/-1';
                warnDiv.innerHTML = `⚠ No pages auto-matched topic keywords. Manually select relevant pages.`;
                container.appendChild(warnDiv);
            }}

            thumbnails.forEach(thumb => {{
                const div = document.createElement('div');
                div.className = 'page-item' + (selectedPages.has(thumb.page) ? ' selected' : '');
                div.innerHTML = `
                    <img src="${{thumb.data}}" onclick="togglePage(${{thumb.page}}, this.parentElement)">
                    <div class="page-number">Page ${{thumb.page}}</div>
                    <button class="page-zoom-btn" onclick="event.stopPropagation(); zoomPage(${{thumb.page}})">🔍</button>
                `;
                container.appendChild(div);
            }});

            // Store thumbnails for collected display
            window.currentThumbnails = thumbnails;

            // Only show manual page selection if AI mode is OFF
            if (!aiModeEnabled) {{
                document.getElementById('pageSection').classList.remove('hidden');
            }}
            document.getElementById('statusBar').classList.remove('hidden');
            updateSelectedCount();
            updateCollectedDisplay();
        }}

        function togglePage(pageNum, element) {{
            if (selectionConfirmed) return;

            if (selectedPages.has(pageNum)) {{
                selectedPages.delete(pageNum);
                element.classList.remove('selected');
            }} else {{
                selectedPages.add(pageNum);
                element.classList.add('selected');
            }}
            updateSelectedCount();
        }}

        function updateSelectedCount() {{
            document.getElementById('selectedCount').textContent = selectedPages.size;
        }}

        function updateCollectedDisplay() {{
            const totalCollected = collectedPages.reduce((sum, p) => sum + p.pages.length, 0);
            const collectedBadge = document.getElementById('collectedBadge');
            const collectedPanel = document.getElementById('collectedPanel');
            const collectedThumbs = document.getElementById('collectedThumbs');

            if (totalCollected > 0) {{
                document.getElementById('collectedCount').textContent = totalCollected;
                collectedBadge.classList.remove('hidden');
                collectedPanel.classList.remove('hidden');

                // Build thumbnails display
                let html = '';
                collectedPages.forEach((cp, cpIndex) => {{
                    cp.pages.forEach((pageNum, pageIndex) => {{
                        const thumb = cp.thumbnails.find(t => t.page === pageNum);
                        if (thumb) {{
                            html += `
                                <div class="collected-thumb" title="${{cp.title}} - Page ${{pageNum}}">
                                    <img src="${{thumb.data}}">
                                    <button class="remove-btn" onclick="removeCollectedPage(${{cpIndex}}, ${{pageNum}})">×</button>
                                </div>
                            `;
                        }}
                    }});
                }});
                collectedThumbs.innerHTML = html;
            }} else {{
                collectedBadge.classList.add('hidden');
                collectedPanel.classList.add('hidden');
            }}
        }}

        function removeCollectedPage(cpIndex, pageNum) {{
            if (cpIndex < collectedPages.length) {{
                collectedPages[cpIndex].pages = collectedPages[cpIndex].pages.filter(p => p !== pageNum);
                if (collectedPages[cpIndex].pages.length === 0) {{
                    collectedPages.splice(cpIndex, 1);
                }}
                updateCollectedDisplay();
            }}
        }}

        function confirmSelection() {{
            if (selectedPages.size === 0) {{
                alert('Please select at least one page');
                return;
            }}

            selectionConfirmed = true;

            // Save current selection to collected pages
            collectedPages.push({{
                pdfPath: currentPDF,
                pages: Array.from(selectedPages).sort((a, b) => a - b),
                title: currentPDFTitle,
                thumbnails: window.currentThumbnails || []
            }});

            // Update UI
            document.getElementById('confirmBtn').classList.add('hidden');
            document.getElementById('editBtn').classList.remove('hidden');
            document.getElementById('generateBtn').classList.remove('hidden');
            document.getElementById('addMoreBtn').classList.remove('hidden');
            document.getElementById('msCheckboxLabel').classList.remove('hidden');

            // Dim unselected pages
            document.querySelectorAll('.page-item').forEach(el => {{
                el.style.pointerEvents = 'none';
                if (!el.classList.contains('selected')) {{
                    el.style.opacity = '0.3';
                }}
            }});

            updateCollectedDisplay();
        }}

        function editSelection() {{
            selectionConfirmed = false;

            // Remove the last collected entry
            if (collectedPages.length > 0) {{
                const lastEntry = collectedPages.pop();
                // Restore selected pages from the entry we just removed
                selectedPages = new Set(lastEntry.pages);
            }}

            // Update UI
            document.getElementById('confirmBtn').classList.remove('hidden');
            document.getElementById('editBtn').classList.add('hidden');
            document.getElementById('generateBtn').classList.add('hidden');
            document.getElementById('addMoreBtn').classList.add('hidden');

            // Re-enable page selection
            document.querySelectorAll('.page-item').forEach(el => {{
                el.style.pointerEvents = 'auto';
                el.style.opacity = '1';
            }});

            updateSelectedCount();
            updateCollectedDisplay();
        }}

        function addMorePDFs() {{
            // Keep collected pages but reset current selection
            selectedPages.clear();
            currentPDF = null;
            selectionConfirmed = false;

            document.getElementById('pageSection').classList.add('hidden');
            document.getElementById('confirmBtn').classList.remove('hidden');
            document.getElementById('editBtn').classList.add('hidden');
            document.getElementById('generateBtn').classList.add('hidden');
            document.getElementById('addMoreBtn').classList.add('hidden');

            updateSelectedCount();
            document.getElementById('pdfResults').scrollIntoView({{ behavior: 'smooth' }});
        }}

        async function generatePDF() {{
            const totalCollected = collectedPages.reduce((sum, p) => sum + p.pages.length, 0);

            if (totalCollected === 0) {{
                alert('Please select at least one page');
                return;
            }}

            document.getElementById('loadingText').textContent = 'Generating PDF...';
            document.getElementById('loading').classList.add('active');

            try {{
                // Check if mark schemes checkbox is checked
                const includeMS = document.getElementById('includeMarkSchemes')?.checked ?? false;

                const response = await fetch('/api/generate-multi', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        collected: collectedPages,
                        topic: selectedTopic,
                        includeMarkSchemes: includeMS
                    }})
                }});

                const blob = await response.blob();
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;

                // Determine filename based on content type (ZIP if mark schemes included)
                const contentType = response.headers.get('Content-Type');
                const safeTopic = selectedTopic.replace(/[^a-zA-Z0-9]/g, '_');
                if (contentType && contentType.includes('zip')) {{
                    a.download = `${{safeTopic}}_Homework.zip`;
                }} else {{
                    a.download = `${{safeTopic}}_Homework.pdf`;
                }}
                a.click();

                // Show success animation
                document.getElementById('loading').classList.remove('active');
                showSuccessAnimation(totalCollected, includeMS);

            }} catch (error) {{
                console.error('Generate error:', error);
                alert('Error generating PDF');
                document.getElementById('loading').classList.remove('active');
            }}
        }}

        function showSuccessAnimation(pageCount, includedMarkSchemes = false) {{
            const modal = document.getElementById('successModal');
            const message = document.getElementById('successMessage');
            if (includedMarkSchemes) {{
                message.textContent = `Downloaded ZIP with ${{pageCount}} question pages + matching mark schemes for ${{selectedTopic}}`;
            }} else {{
                message.textContent = `Successfully generated ${{pageCount}} page${{pageCount > 1 ? 's' : ''}} for ${{selectedTopic}}`;
            }}

            // Add confetti pieces
            const content = modal.querySelector('.success-content');
            const colors = ['var(--primary)', 'var(--secondary)', 'var(--success)', 'var(--warning)'];

            for (let i = 0; i < 20; i++) {{
                const confetti = document.createElement('div');
                confetti.className = 'confetti-piece';
                confetti.style.left = Math.random() * 100 + '%';
                confetti.style.top = Math.random() * 100 + '%';
                confetti.style.background = colors[Math.floor(Math.random() * colors.length)];
                confetti.style.animationDelay = Math.random() * 0.5 + 's';
                content.appendChild(confetti);
            }}

            modal.classList.remove('hidden');

            // Remove confetti after animation
            setTimeout(() => {{
                content.querySelectorAll('.confetti-piece').forEach(c => c.remove());
            }}, 2000);
        }}

        function closeSuccessModal() {{
            document.getElementById('successModal').classList.add('hidden');
        }}

        async function zoomPage(pageNum) {{
            try {{
                const response = await fetch('/api/zoom-page', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ path: currentPDF, page: pageNum }})
                }});

                const data = await response.json();
                document.getElementById('zoomImage').src = data.image;
                document.getElementById('zoomModal').classList.remove('hidden');
            }} catch (error) {{
                console.error('Zoom error:', error);
            }}
        }}

        function closeZoom() {{
            document.getElementById('zoomModal').classList.add('hidden');
        }}

        async function viewAIPageZoom(pdfPath, pageNum) {{
            try {{
                const response = await fetch('/api/zoom-page', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ path: pdfPath, page: pageNum }})
                }});

                const data = await response.json();
                document.getElementById('zoomImage').src = data.image;
                document.getElementById('zoomModal').classList.remove('hidden');
            }} catch (error) {{
                console.error('Zoom error:', error);
            }}
        }}

        // Event delegation for AI page thumb clicks
        document.addEventListener('click', function(event) {{
            // Check if clicked on ai-page-thumb or its children (but not remove button)
            const thumb = event.target.closest('.ai-page-thumb');
            if (thumb && !event.target.classList.contains('remove-page')) {{
                const pdfPath = thumb.dataset.path;
                const pageNum = parseInt(thumb.dataset.page);
                if (pdfPath && pageNum) {{
                    viewAIPageZoom(pdfPath, pageNum);
                }}
            }}

            // Check if clicked on custom zoom button
            if (event.target.classList.contains('zoom-btn-custom')) {{
                event.stopPropagation();
                const pageNum = parseInt(event.target.dataset.page);
                if (pageNum) {{
                    viewCustomPageZoom(pageNum);
                }}
            }}
        }});

        async function viewCustomPageZoom(pageNum) {{
            if (!window.currentCustomPdfPath) {{
                console.error('No custom PDF path set');
                return;
            }}

            try {{
                const response = await fetch('/api/zoom-page', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ path: window.currentCustomPdfPath, page: pageNum }})
                }});

                const data = await response.json();
                document.getElementById('zoomImage').src = data.image;
                document.getElementById('zoomModal').classList.remove('hidden');
            }} catch (error) {{
                console.error('Custom page zoom error:', error);
            }}
        }}

        // Mark Schemes toggle (button-based)
        let markSchemesVisible = false;

        function toggleMarkSchemesBtn() {{
            markSchemesVisible = !markSchemesVisible;
            const btn = document.getElementById('markSchemeToggle');
            btn.classList.toggle('active', markSchemesVisible);
            document.querySelectorAll('.ms-btn').forEach(el => {{
                el.style.display = markSchemesVisible ? '' : 'none';
            }});
        }}

        // Legacy function for backwards compatibility
        function toggleMarkSchemes() {{
            toggleMarkSchemesBtn();
        }}

        // AI-Enhanced Mode variables
        let aiModeEnabled = false;
        let selectedPapersForAI = new Set();  // Stores indices of selected papers

        // Global AI Mode toggle (from the banner at top)
        function toggleAIModeGlobal() {{
            aiModeEnabled = !aiModeEnabled;
            const toggleBtn = document.getElementById('aiToggleBtn');
            const disclaimer = document.getElementById('aiDisclaimer');

            toggleBtn.classList.toggle('active', aiModeEnabled);
            toggleBtn.querySelector('.toggle-label').textContent = aiModeEnabled ? 'Enabled' : 'Enable';
            disclaimer.classList.toggle('hidden', !aiModeEnabled);

            // Hide manual page selection when AI mode is enabled
            const pageSection = document.getElementById('pageSection');
            if (aiModeEnabled) {{
                pageSection.classList.add('hidden');
            }}

            // Update paper buttons if results are visible
            const processBtn = document.getElementById('aiProcessBtn');
            if (processBtn) {{
                if (aiModeEnabled) {{
                    processBtn.style.display = '';
                    document.querySelectorAll('.qp-btn').forEach(btn => {{
                        btn.classList.add('ai-selectable');
                    }});
                    selectedPapersForAI.clear();
                    updateAIProcessButton();
                }} else {{
                    processBtn.style.display = 'none';
                    document.querySelectorAll('.qp-btn').forEach(btn => {{
                        btn.classList.remove('ai-selectable', 'ai-selected');
                    }});
                    selectedPapersForAI.clear();
                }}
            }}
        }}

        // Legacy function
        function toggleAIMode() {{
            toggleAIModeGlobal();
        }}

        function togglePaperForAI(index, btn) {{
            if (selectedPapersForAI.has(index)) {{
                selectedPapersForAI.delete(index);
                btn.classList.remove('ai-selected');
            }} else {{
                selectedPapersForAI.add(index);
                btn.classList.add('ai-selected');
            }}
            updateAIProcessButton();
        }}

        function updateAIProcessButton() {{
            const count = selectedPapersForAI.size;
            document.getElementById('selectedPaperCount').textContent = count;
            const btn = document.getElementById('aiProcessBtn');
            btn.disabled = count === 0;
            btn.style.opacity = count === 0 ? '0.5' : '1';
        }}

        async function processAIPapers() {{
            if (selectedPapersForAI.size === 0) return;
            if (!selectedTopic) {{
                alert('Please select a topic first');
                return;
            }}

            // Keep results section visible, show loading progress BELOW the Found PDFs
            document.getElementById('loadingProgress').classList.remove('hidden');

            // Reset progress steps
            for (let i = 1; i <= 4; i++) {{
                const step = document.getElementById(`loadingStep${{i}}`);
                step.classList.remove('active', 'done');
            }}
            document.getElementById('loadingStep1').classList.add('active');

            // Scroll to show the progress steps
            document.getElementById('loadingProgress').scrollIntoView({{ behavior: 'smooth', block: 'center' }});

            try {{
                // Get the selected paper URLs
                const selectedPapers = Array.from(selectedPapersForAI).map(idx => window.pdfResults[idx]);

                // Simulate progress updates (the backend processes all at once, but we show progress)
                setTimeout(() => {{
                    document.getElementById('loadingStep1').classList.remove('active');
                    document.getElementById('loadingStep1').classList.add('done');
                    document.getElementById('loadingStep2').classList.add('active');
                }}, 1000);

                setTimeout(() => {{
                    document.getElementById('loadingStep2').classList.remove('active');
                    document.getElementById('loadingStep2').classList.add('done');
                    document.getElementById('loadingStep3').classList.add('active');
                }}, 3000);

                const response = await fetch('/api/ai-process-papers', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        papers: selectedPapers.map(p => ({{ url: p.url, title: p.title }})),
                        topic: selectedTopic
                    }})
                }});

                // Mark remaining steps done
                document.getElementById('loadingStep3').classList.remove('active');
                document.getElementById('loadingStep3').classList.add('done');
                document.getElementById('loadingStep4').classList.add('active');

                const data = await response.json();

                document.getElementById('loadingStep4').classList.remove('active');
                document.getElementById('loadingStep4').classList.add('done');

                if (data.error) {{
                    alert('Error processing papers: ' + data.error);
                    document.getElementById('loadingProgress').classList.add('hidden');
                    return;
                }}

                // Small delay to show completion
                await new Promise(resolve => setTimeout(resolve, 500));

                // Display all processed papers with auto-selected pages
                displayAIResults(data.results);

            }} catch (error) {{
                console.error('AI processing error:', error);
                alert('Error processing papers with AI: ' + error.message);
            }}

            document.getElementById('loadingProgress').classList.add('hidden');
        }}

        function displayAIResults(results) {{
            console.log('displayAIResults called with:', results);

            // Clear previous collected pages and add AI-detected pages
            collectedPages = [];
            loadedPDFs = [];

            if (!results || !Array.isArray(results)) {{
                console.error('Invalid results:', results);
                alert('Error: Invalid results from AI processing');
                return;
            }}

            let totalPagesFound = 0;

            results.forEach((paperResult, idx) => {{
                console.log(`Processing paper ${{idx}}:`, paperResult.title, 'filtered_pages:', paperResult.filtered_pages);

                loadedPDFs.push({{
                    path: paperResult.path,
                    url: paperResult.url,
                    title: paperResult.title,
                    thumbnails: paperResult.thumbnails
                }});

                // Auto-add the AI-detected pages to collected (grouped by PDF)
                // Handle new format (objects with confidence) or old format (just page numbers)
                if (paperResult.filtered_pages && paperResult.filtered_pages.length > 0) {{
                    const validPages = paperResult.filtered_pages
                        .map(p => typeof p === 'object' ? p.page + 1 : p)
                        .filter(pageNum => pageNum > 0 && pageNum <= paperResult.thumbnails.length);

                    if (validPages.length > 0) {{
                        collectedPages.push({{
                            pdfPath: paperResult.path,
                            pages: validPages,
                            title: paperResult.title,
                            thumbnails: paperResult.thumbnails
                        }});
                        totalPagesFound += validPages.length;
                    }}
                }}
            }});

            console.log('Collected page groups:', collectedPages.length, 'Total pages:', totalPagesFound);

            // Build the AI Results Panel (instead of alert)
            buildAIResultsPanel(results, totalPagesFound);

            // Show the status bar and buttons
            document.getElementById('statusBar').classList.remove('hidden');
            document.getElementById('confirmBtn').classList.add('hidden');
            document.getElementById('editBtn').classList.remove('hidden');
            document.getElementById('generateBtn').classList.remove('hidden');
            document.getElementById('addMoreBtn').classList.remove('hidden');
            document.getElementById('msCheckboxLabel').classList.remove('hidden');
            selectionConfirmed = true;

            // Update collected display
            updateCollectedDisplay();

            // Scroll to results
            setTimeout(() => {{
                document.getElementById('aiResultsPanel').scrollIntoView({{ behavior: 'smooth', block: 'start' }});
            }}, 100);
        }}

        function buildAIResultsPanel(results, totalPages) {{
            const panel = document.getElementById('aiResultsPanel');
            const papersList = document.getElementById('aiPapersList');

            // Update header stats
            document.getElementById('aiResultsTopic').textContent = selectedTopic;
            document.getElementById('aiTotalPages').textContent = totalPages;
            document.getElementById('aiTotalPapers').textContent = results.length;

            // Build papers list
            let html = '';
            results.forEach((paperResult, paperIdx) => {{
                const filteredPages = paperResult.filtered_pages || [];
                const hasPages = filteredPages.length > 0;

                html += `
                    <div class="ai-paper-item">
                        <div class="ai-paper-header">
                            <span class="ai-paper-title">${{paperResult.title}}</span>
                            <span class="ai-paper-pages-count">${{filteredPages.length}} page${{filteredPages.length !== 1 ? 's' : ''}} found</span>
                        </div>
                        <div class="ai-paper-pages">
                `;

                if (hasPages) {{
                    filteredPages.forEach(pageData => {{
                        // Handle both old format (just page number) and new format (object with confidence)
                        const pageNum = typeof pageData === 'object' ? pageData.page + 1 : pageData;
                        const confidence = typeof pageData === 'object' ? pageData.confidence : 'high';
                        const thumb = paperResult.thumbnails[pageNum - 1];
                        if (thumb) {{
                            html += `
                                <div class="ai-page-thumb ${{confidence}}-confidence" data-paper="${{paperIdx}}" data-page="${{pageNum}}" data-path="${{paperResult.path}}">
                                    <img src="${{thumb.data}}" alt="Page ${{pageNum}}">
                                    <div class="confidence-indicator ${{confidence}}">${{confidence === 'high' ? 'Definite' : 'Maybe'}}</div>
                                    <div class="zoom-overlay">
                                        <div class="zoom-icon">🔍</div>
                                    </div>
                                    <div class="page-label">Page ${{pageNum}}</div>
                                    <button class="remove-page" onclick="removeAIPage(${{paperIdx}}, ${{pageNum}}, event)">×</button>
                                </div>
                            `;
                        }}
                    }});
                }} else {{
                    html += `<div class="ai-no-pages">No matching pages found in this paper</div>`;
                }}

                html += `
                        </div>
                    </div>
                `;
            }});

            papersList.innerHTML = html;
            panel.classList.remove('hidden');
        }}

        function removeAIPage(paperIdx, pageNum, event) {{
            event.stopPropagation();

            // Find and remove from collectedPages
            for (let i = 0; i < collectedPages.length; i++) {{
                const cp = collectedPages[i];
                const pageIndex = cp.pages.indexOf(pageNum);
                if (pageIndex > -1 && loadedPDFs[paperIdx] && cp.pdfPath === loadedPDFs[paperIdx].path) {{
                    cp.pages.splice(pageIndex, 1);
                    if (cp.pages.length === 0) {{
                        collectedPages.splice(i, 1);
                    }}
                    break;
                }}
            }}

            // Remove the visual element
            event.target.closest('.ai-page-thumb').remove();

            // Update stats
            const totalPages = collectedPages.reduce((sum, cp) => sum + cp.pages.length, 0);
            document.getElementById('aiTotalPages').textContent = totalPages;

            // Update collected display
            updateCollectedDisplay();
        }}

        function startOver() {{
            selectedTopic = null;
            selectedPages.clear();
            currentPDF = null;
            selectionConfirmed = false;
            collectedPages = [];
            loadedPDFs = [];

            document.querySelectorAll('.topic-item').forEach(el => el.classList.remove('selected'));
            document.getElementById('keywords').value = '';
            document.getElementById('resultsSection').classList.add('hidden');
            document.getElementById('pageSection').classList.add('hidden');
            document.getElementById('statusBar').classList.add('hidden');
            document.getElementById('collectedPanel').classList.add('hidden');
            document.getElementById('confirmBtn').classList.remove('hidden');
            document.getElementById('editBtn').classList.add('hidden');
            document.getElementById('generateBtn').classList.add('hidden');
            document.getElementById('addMoreBtn').classList.add('hidden');
            document.getElementById('collectedBadge').classList.add('hidden');
            document.getElementById('msCheckboxLabel').classList.add('hidden');
            document.getElementById('aiResultsPanel').classList.add('hidden');

            fetch('/api/cleanup', {{ method: 'POST' }});
        }}

        document.addEventListener('keydown', e => {{
            if (e.key === 'Escape') closeZoom();
        }});

        // Custom Select Dropdown Functions
        function toggleCustomSelect(selectId) {{
            const select = document.getElementById(selectId);
            const isOpen = select.classList.contains('open');

            // Close all other dropdowns first
            document.querySelectorAll('.custom-select.open').forEach(s => {{
                if (s.id !== selectId) s.classList.remove('open');
            }});

            // Toggle this one
            select.classList.toggle('open');
        }}

        function selectOption(selectId, value, label) {{
            const select = document.getElementById(selectId);
            const trigger = select.querySelector('.custom-select-value');
            const hiddenInput = select.nextElementSibling;

            // Update display
            trigger.textContent = label;
            trigger.dataset.value = value;

            // Update hidden input
            if (hiddenInput && hiddenInput.tagName === 'INPUT') {{
                hiddenInput.value = value;
            }}

            // Update selected state
            select.querySelectorAll('.custom-select-option').forEach(opt => {{
                opt.classList.remove('selected');
                if (opt.dataset.value === value) {{
                    opt.classList.add('selected');
                }}
            }});

            // Close dropdown
            select.classList.remove('open');
        }}

        // Close dropdowns when clicking outside
        document.addEventListener('click', function(e) {{
            if (!e.target.closest('.custom-select')) {{
                document.querySelectorAll('.custom-select.open').forEach(s => {{
                    s.classList.remove('open');
                }});
            }}
        }});

        // Theme switching
        function setTheme(theme) {{
            document.documentElement.setAttribute('data-theme', theme);
            localStorage.setItem('homework-theme', theme);

            document.querySelectorAll('.theme-btn').forEach(btn => btn.classList.remove('active'));
            document.getElementById('theme-' + theme).classList.add('active');
        }}

        // Load saved theme
        (function() {{
            const savedTheme = localStorage.getItem('homework-theme') || 'default';
            setTheme(savedTheme);
        }})();

        // Enhanced Custom Cursor System with dot, ring, and glow
        (function() {{
            const cursorDot = document.getElementById('cursorDot');
            const cursorRing = document.getElementById('cursorRing');
            const cursorGlow = document.getElementById('cursorGlow');

            let mouseX = 0, mouseY = 0;
            let dotX = 0, dotY = 0;
            let ringX = 0, ringY = 0;
            let glowX = 0, glowY = 0;

            document.addEventListener('mousemove', (e) => {{
                mouseX = e.clientX;
                mouseY = e.clientY;
            }});

            // Smooth animation loop with different speeds for each element
            function animate() {{
                // Dot follows closely (fast)
                dotX += (mouseX - dotX) * 0.35;
                dotY += (mouseY - dotY) * 0.35;
                cursorDot.style.left = dotX + 'px';
                cursorDot.style.top = dotY + 'px';

                // Ring follows with medium lag
                ringX += (mouseX - ringX) * 0.15;
                ringY += (mouseY - ringY) * 0.15;
                cursorRing.style.left = ringX + 'px';
                cursorRing.style.top = ringY + 'px';

                // Glow follows with heavy lag
                glowX += (mouseX - glowX) * 0.08;
                glowY += (mouseY - glowY) * 0.08;
                cursorGlow.style.left = glowX + 'px';
                cursorGlow.style.top = glowY + 'px';

                requestAnimationFrame(animate);
            }}

            animate();

            // Detect hover on interactive elements
            const hoverElements = 'button, a, .topic-item, .qp-btn, .ms-btn, .pdf-card, .page-card, .theme-btn, select, input';
            document.addEventListener('mouseover', (e) => {{
                if (e.target.matches(hoverElements) || e.target.closest(hoverElements)) {{
                    cursorRing.classList.add('hover');
                    cursorDot.style.transform = 'translate(-50%, -50%) scale(1.5)';
                }}
            }});

            document.addEventListener('mouseout', (e) => {{
                if (e.target.matches(hoverElements) || e.target.closest(hoverElements)) {{
                    cursorRing.classList.remove('hover');
                    cursorDot.style.transform = 'translate(-50%, -50%) scale(1)';
                }}
            }});

            // Click effect
            document.addEventListener('mousedown', () => {{
                cursorDot.classList.add('clicking');
                cursorRing.classList.add('clicking');
            }});

            document.addEventListener('mouseup', () => {{
                cursorDot.classList.remove('clicking');
                cursorRing.classList.remove('clicking');
            }});

            // Hide cursor elements when mouse leaves window
            document.addEventListener('mouseleave', () => {{
                cursorDot.style.opacity = '0';
                cursorRing.style.opacity = '0';
                cursorGlow.style.opacity = '0';
            }});

            document.addEventListener('mouseenter', () => {{
                cursorDot.style.opacity = '1';
                cursorRing.style.opacity = '0.6';
                cursorGlow.style.opacity = '0.6';
            }});

            // Hide default cursor on body
            document.body.style.cursor = 'none';
            document.querySelectorAll('*').forEach(el => el.style.cursor = 'none');
        }})();

        // Add stagger animation to topic items
        setTimeout(() => {{
            document.querySelectorAll('.topic-item').forEach((item, index) => {{
                item.style.animationDelay = (index * 0.03) + 's';
                item.classList.add('animate-fade-in');
            }});
        }}, 100);

        // ============================================
        // CUSTOM RESOURCES FUNCTIONALITY
        // ============================================

        let customPdfFile = null;
        let customPdfPath = null;
        let customSelectedTopic = null;
        let customSelectedPages = new Set();
        let customPageData = [];

        // Populate custom topic grid (same topics as main)
        const customTopicGrid = document.getElementById('customTopicGrid');
        TOPICS.forEach(topic => {{
            const div = document.createElement('div');
            div.className = 'topic-item';
            div.textContent = topic;
            div.onclick = () => selectCustomTopic(topic, div);
            customTopicGrid.appendChild(div);
        }});

        // Tab switching
        function switchMainTab(tab) {{
            const pastPapersTab = document.getElementById('tabPastPapers');
            const customTab = document.getElementById('tabCustomResources');
            const pastPapersContent = document.getElementById('pastPapersContent');
            const customContent = document.getElementById('customResourcesContent');

            if (tab === 'pastpapers') {{
                pastPapersTab.classList.add('active');
                customTab.classList.remove('active');
                pastPapersContent.style.display = 'block';
                customContent.classList.remove('active');
            }} else {{
                pastPapersTab.classList.remove('active');
                customTab.classList.add('active');
                pastPapersContent.style.display = 'none';
                customContent.classList.add('active');
            }}
        }}

        // Drag and drop handling
        const uploadZone = document.getElementById('uploadZone');

        uploadZone.addEventListener('dragover', (e) => {{
            e.preventDefault();
            uploadZone.classList.add('drag-over');
        }});

        uploadZone.addEventListener('dragleave', (e) => {{
            e.preventDefault();
            uploadZone.classList.remove('drag-over');
        }});

        uploadZone.addEventListener('drop', (e) => {{
            e.preventDefault();
            uploadZone.classList.remove('drag-over');
            const files = e.dataTransfer.files;
            if (files.length > 0 && files[0].type === 'application/pdf') {{
                handleCustomPdfFile(files[0]);
            }}
        }});

        // Handle PDF upload
        function handleCustomPdfUpload(event) {{
            const file = event.target.files[0];
            if (file && file.type === 'application/pdf') {{
                handleCustomPdfFile(file);
            }}
        }}

        async function handleCustomPdfFile(file) {{
            customPdfFile = file;

            // Show loading
            document.getElementById('uploadZone').style.display = 'none';
            document.getElementById('uploadedPdfInfo').classList.remove('hidden');
            document.getElementById('uploadedPdfName').textContent = file.name;
            document.getElementById('uploadedPdfMeta').textContent = 'Uploading...';

            // Upload file to server
            const formData = new FormData();
            formData.append('file', file);

            try {{
                const response = await fetch('/upload_custom_pdf', {{
                    method: 'POST',
                    body: formData
                }});

                const data = await response.json();
                if (data.success) {{
                    customPdfPath = data.path;
                    window.currentCustomPdfPath = data.path; // Store for zoom functionality
                    const sizeMB = (file.size / (1024 * 1024)).toFixed(2);
                    document.getElementById('uploadedPdfMeta').textContent = `${{data.page_count}} pages • ${{sizeMB}} MB`;

                    // Show topic selection and scan button
                    document.getElementById('customTopicSection').classList.remove('hidden');
                    document.getElementById('scanBtn').classList.remove('hidden');
                }} else {{
                    alert('Error uploading PDF: ' + data.error);
                    removeUploadedPdf();
                }}
            }} catch (error) {{
                alert('Error uploading PDF: ' + error.message);
                removeUploadedPdf();
            }}
        }}

        function removeUploadedPdf() {{
            customPdfFile = null;
            customPdfPath = null;
            customSelectedTopic = null;
            document.getElementById('uploadZone').style.display = 'block';
            document.getElementById('uploadedPdfInfo').classList.add('hidden');
            document.getElementById('customTopicSection').classList.add('hidden');
            document.getElementById('scanBtn').classList.add('hidden');
            document.getElementById('customResultsSection').classList.add('hidden');
            document.getElementById('customPdfInput').value = '';

            // Reset topic selection
            document.querySelectorAll('#customTopicGrid .topic-item').forEach(el => {{
                el.classList.remove('selected');
            }});
        }}

        function selectCustomTopic(topic, element) {{
            // Deselect previous
            document.querySelectorAll('#customTopicGrid .topic-item').forEach(el => {{
                el.classList.remove('selected');
            }});

            // Select new
            element.classList.add('selected');
            customSelectedTopic = topic;

            // Enable scan button
            const scanBtn = document.getElementById('scanBtn');
            scanBtn.disabled = false;
            scanBtn.querySelector('span:last-child').textContent = `Scan PDF for "${{topic}}"`;
        }}

        async function scanCustomPdf() {{
            if (!customPdfPath || !customSelectedTopic) return;

            // Show scanning overlay
            const overlay = document.createElement('div');
            overlay.className = 'scanning-overlay';
            overlay.id = 'scanningOverlay';
            overlay.innerHTML = `
                <div class="scanning-animation">
                    <div class="scanning-circle"></div>
                    <div class="scanning-circle"></div>
                    <div class="scanning-circle"></div>
                    <div class="scanning-icon">🔍</div>
                </div>
                <p class="scanning-text">Scanning pages for "${{customSelectedTopic}}"...</p>
                <p class="scanning-subtext">Analysing text content on each page</p>
            `;
            document.body.appendChild(overlay);

            try {{
                const response = await fetch('/scan_custom_pdf', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        path: customPdfPath,
                        topic: customSelectedTopic
                    }})
                }});

                const data = await response.json();
                document.getElementById('scanningOverlay').remove();

                if (data.success) {{
                    displayCustomResults(data);
                }} else {{
                    alert('Error scanning PDF: ' + data.error);
                }}
            }} catch (error) {{
                document.getElementById('scanningOverlay').remove();
                alert('Error scanning PDF: ' + error.message);
            }}
        }}

        function displayCustomResults(data) {{
            customPageData = data.pages;
            customSelectedPages = new Set();

            const highConfPages = data.pages.filter(p => p.confidence === 'high');
            const mediumConfPages = data.pages.filter(p => p.confidence === 'medium');

            // Auto-select high confidence pages
            highConfPages.forEach(p => customSelectedPages.add(p.page));

            // Update stats
            document.getElementById('customResultsText').textContent =
                `Found ${{highConfPages.length}} definite + ${{mediumConfPages.length}} possible pages for "${{customSelectedTopic}}"`;

            // Build page grid
            const grid = document.getElementById('customPageGrid');
            grid.innerHTML = '';

            data.pages.forEach(page => {{
                const isSelected = customSelectedPages.has(page.page);
                const card = document.createElement('div');
                card.className = `custom-page-card ${{page.confidence}}-confidence ${{isSelected ? 'selected' : ''}}`;
                card.dataset.page = page.page;

                card.innerHTML = `
                    <img class="custom-page-thumb" src="data:image/png;base64,${{page.thumbnail}}" alt="Page ${{page.page}}">
                    <div class="confidence-badge ${{page.confidence}}">${{page.confidence === 'high' ? 'Definite' : 'Maybe'}}</div>
                    <div class="page-number-badge">Page ${{page.page}}</div>
                    <div class="select-overlay">
                        <div class="select-check">✓</div>
                    </div>
                    <button class="zoom-btn-custom" data-page="${{page.page}}" title="View full page">🔍</button>
                `;

                // Add click handler to card (but not zoom button)
                card.addEventListener('click', function(e) {{
                    if (!e.target.classList.contains('zoom-btn-custom')) {{
                        toggleCustomPage(page.page, card);
                    }}
                }});

                grid.appendChild(card);
            }});

            // Show results section
            document.getElementById('customResultsSection').classList.remove('hidden');

            // Update status bar
            updateCustomStatusBar();

            // Show status bar
            document.getElementById('statusBar').classList.remove('hidden');
        }}

        function toggleCustomPage(pageNum, card) {{
            if (customSelectedPages.has(pageNum)) {{
                customSelectedPages.delete(pageNum);
                card.classList.remove('selected');
            }} else {{
                customSelectedPages.add(pageNum);
                card.classList.add('selected');
            }}
            updateCustomStatusBar();
        }}

        function updateCustomStatusBar() {{
            document.getElementById('selectedCount').textContent = customSelectedPages.size;
        }}

        function resetCustomResources() {{
            customSelectedPages = new Set();
            customPageData = [];
            document.getElementById('customResultsSection').classList.add('hidden');
            document.getElementById('statusBar').classList.add('hidden');

            // Reset topic selection
            customSelectedTopic = null;
            document.querySelectorAll('#customTopicGrid .topic-item').forEach(el => {{
                el.classList.remove('selected');
            }});
            document.getElementById('scanBtn').disabled = true;
            document.getElementById('scanBtn').querySelector('span:last-child').textContent = 'Scan PDF for Topic';
        }}

        // Override generatePDF to handle custom resources mode
        const originalGeneratePDF = generatePDF;
        generatePDF = async function() {{
            // Check if we're in custom resources mode
            if (document.getElementById('customResourcesContent').classList.contains('active') && customSelectedPages.size > 0) {{
                await generateCustomPDF();
            }} else {{
                await originalGeneratePDF();
            }}
        }};

        async function generateCustomPDF() {{
            if (customSelectedPages.size === 0) {{
                alert('Please select at least one page');
                return;
            }}

            document.getElementById('loading').classList.remove('hidden');
            document.getElementById('loadingText').textContent = 'Generating your filtered PDF...';

            try {{
                const response = await fetch('/generate_custom_pdf', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        path: customPdfPath,
                        pages: Array.from(customSelectedPages).sort((a, b) => a - b),
                        topic: customSelectedTopic
                    }})
                }});

                const data = await response.json();
                document.getElementById('loading').classList.add('hidden');

                if (data.success) {{
                    // Show success modal
                    document.getElementById('successMessage').textContent =
                        `${{customSelectedPages.size}} pages extracted for "${{customSelectedTopic}}"`;
                    document.getElementById('successModal').classList.remove('hidden');

                    // Trigger download
                    const link = document.createElement('a');
                    link.href = data.download_url;
                    link.download = data.filename;
                    link.click();
                }} else {{
                    alert('Error generating PDF: ' + data.error);
                }}
            }} catch (error) {{
                document.getElementById('loading').classList.add('hidden');
                alert('Error generating PDF: ' + error.message);
            }}
        }}
    </script>
</body>
</html>'''
