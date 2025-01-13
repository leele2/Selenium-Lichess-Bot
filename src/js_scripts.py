def remove_arrow_script(width, height, move):
    script = """
        // Find all elements with the specified class name
        const existingElements = document.querySelectorAll('.cg-shapes');
        
        // Loop through each existing element
        existingElements.forEach(element => {
          // Find all <g> tags inside each existing element
          const gTags = element.querySelectorAll('g');
        
          // Loop through each <g> tag and remove it
          gTags.forEach(gTag => {
            gTag.remove();
          });
        });
        """
    return script

def generate_arrow_script(width:int, height:int, move:str, areBlack:bool):
    xmap = {i:(-3.5 + n) for (n,i) in enumerate(list(map(chr, range(97, 97+8))))}
    ymap = {i:(4.5 - i) for i in range(1,9)}
    if areBlack:
        c = -1
    else:
        c = 1
    before_x = c * xmap[move[0]]
    before_y = c * ymap[int(move[1])]
    after_x = c * xmap[move[2]]
    after_y = c * ymap[int(move[3])]
    # javascript script constructed using above variables to be dynamic
    script = [
        "// Find all elements with the specified class name",
        "const existingElements = document.querySelectorAll('.cg-shapes');",
        
        "// Add marker definition for the arrowhead if it doesn't exist",
        "existingElements.forEach(element => {",
        "  const svgRoot = element.closest('svg');",
        "  if (svgRoot && !svgRoot.querySelector('#arrowhead-g')) {",
        "    const defs = svgRoot.querySelector('defs') || document.createElementNS('http://www.w3.org/2000/svg', 'defs');",
        "    if (!svgRoot.querySelector('defs')) {",
        "      svgRoot.appendChild(defs);",
        "    }",
        "    const marker = document.createElementNS('http://www.w3.org/2000/svg', 'marker');",
        "    marker.setAttribute('id', 'arrowhead-g');",
        "    marker.setAttribute('orient', 'auto');",
        "    marker.setAttribute('overflow', 'visible');",
        "    marker.setAttribute('markerWidth', '4');",
        "    marker.setAttribute('markerHeight', '4');",
        "    marker.setAttribute('refX', '2.05');",
        "    marker.setAttribute('refY', '2');",
        "    marker.setAttribute('cgKey', 'g');",
        "    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');",
        "    path.setAttribute('d', 'M0,0 V4 L3,2 Z');",
        "    path.setAttribute('fill', '#15781B');",
        "    marker.appendChild(path);",
        "    defs.appendChild(marker);",
        "  }",
        "});",
        
        "// Loop through each existing element and add a <g> tag inside it",
        "existingElements.forEach(element => {",
        "  const gTag = document.createElementNS('http://www.w3.org/2000/svg', 'g');",
        "  element.appendChild(gTag);",
        
        "  // Add attributes to the nested <g> tag",
        f"  gTag.setAttribute('cgHash', '{width},{height},{move[:2]},{move[-2:]},BROWN');",
        
        "  // Create and append the <line> tag inside the nested <g> tag",
        "  const lineTag = document.createElementNS('http://www.w3.org/2000/svg', 'line');",
        "  lineTag.setAttribute('stroke', '#422805');",
        "  lineTag.setAttribute('stroke-width', '0.15625');",
        "  lineTag.setAttribute('stroke-linecap', 'round');",
        "  lineTag.setAttribute('marker-end', 'url(#arrowhead-g)');",
        "  lineTag.setAttribute('opacity', '1');",
        f"  lineTag.setAttribute('x1', '{before_x}');",
        f"  lineTag.setAttribute('y1', '{before_y}');",
        f"  lineTag.setAttribute('x2', '{after_x}');",
        f"  lineTag.setAttribute('y2', '{after_y}');",
        "  gTag.appendChild(lineTag);",
        "});"
    ]
    return "\n".join(script)