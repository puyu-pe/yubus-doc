;(function installYubusCaptureAnnotations(window) {
  'use strict'

  const namespace = 'yubus-capture-annotations'
  const coral = '#ff5b70'

  function resolve(value) {
    if (typeof value === 'string') return document.querySelector(value)
    return value instanceof Element ? value : null
  }

  function visibleRect(element, rootRect) {
    const style = window.getComputedStyle(element)
    const rect = element.getBoundingClientRect()
    const inViewport = rect.left >= 0 && rect.top >= 0 && rect.right <= window.innerWidth && rect.bottom <= window.innerHeight
    const inRoot = rect.left >= rootRect.left && rect.top >= rootRect.top && rect.right <= rootRect.right && rect.bottom <= rootRect.bottom

    return style.display !== 'none' && style.visibility !== 'hidden' && Number(style.opacity) !== 0 && rect.width > 0 && rect.height > 0 && inViewport && inRoot ? rect : null
  }

  function clear() {
    document.getElementById(namespace)?.remove()
  }

  function render({ root, highlights = [], arrows = [] } = {}) {
    clear()

    const rootElement = resolve(root)
    if (!rootElement) return { ok: false, errors: ['Capture root was not found.'] }

    const rootRect = visibleRect(rootElement, rootElement.getBoundingClientRect())
    if (!rootRect) return { ok: false, errors: ['Capture root is hidden or outside the viewport.'] }

    const targets = new Map()
    const errors = []
    const addTarget = (value) => {
      if (targets.has(value)) return
      const element = resolve(value)
      const rect = element && rootElement.contains(element) ? visibleRect(element, rootRect) : null
      if (!rect) errors.push(`Capture target is unavailable: ${String(value)}`)
      else targets.set(value, rect)
    }

    highlights.forEach(addTarget)
    arrows.forEach(({ from, to }) => {
      addTarget(from)
      addTarget(to)
    })
    arrows.forEach(({ from, to }) => {
      const start = targets.get(from)
      const end = targets.get(to)
      if (!start || !end) return
      const overlap = start.left <= end.right && start.right >= end.left && start.top <= end.bottom && start.bottom >= end.top
      if (from === to || overlap) errors.push('Arrow endpoints must be separate, non-overlapping elements.')
    })
    if (errors.length) return { ok: false, errors }

    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg')
    svg.id = namespace
    svg.setAttribute('aria-hidden', 'true')
    svg.setAttribute('viewBox', `0 0 ${rootRect.width} ${rootRect.height}`)
    Object.assign(svg.style, {
      position: 'fixed', left: `${rootRect.left}px`, top: `${rootRect.top}px`,
      width: `${rootRect.width}px`, height: `${rootRect.height}px`,
      pointerEvents: 'none', zIndex: '2147483647', overflow: 'hidden',
    })

    const make = (name, attributes) => {
      const node = document.createElementNS('http://www.w3.org/2000/svg', name)
      Object.entries(attributes).forEach(([key, value]) => node.setAttribute(key, String(value)))
      svg.append(node)
      return node
    }
    const local = (rect) => ({ x: rect.left - rootRect.left, y: rect.top - rootRect.top })
    const frame = (rect) => {
      const point = local(rect)
      const inset = 1
      const left = Math.max(inset, point.x - 3)
      const top = Math.max(inset, point.y - 3)
      const right = Math.min(rootRect.width - inset, point.x + rect.width + 3)
      const bottom = Math.min(rootRect.height - inset, point.y + rect.height + 3)
      return { x: left, y: top, width: right - left, height: bottom - top }
    }
    const edge = (rect, dx, dy) => {
      const centerX = rect.left - rootRect.left + rect.width / 2
      const centerY = rect.top - rootRect.top + rect.height / 2
      const scale = Math.min(dx === 0 ? Infinity : rect.width / 2 / Math.abs(dx), dy === 0 ? Infinity : rect.height / 2 / Math.abs(dy))
      return { x: centerX + dx * scale, y: centerY + dy * scale }
    }

    highlights.forEach((target) => {
      const rect = targets.get(target)
      make('rect', { ...frame(rect), fill: 'none', stroke: coral, 'stroke-width': 2, rx: 3 })
    })
    arrows.forEach(({ from, to }) => {
      const start = targets.get(from)
      const end = targets.get(to)
      const startCenter = local(start)
      const endCenter = local(end)
      const dx = endCenter.x + end.width / 2 - startCenter.x - start.width / 2
      const dy = endCenter.y + end.height / 2 - startCenter.y - start.height / 2
      const length = Math.hypot(dx, dy)
      const gap = 4
      const source = edge(start, dx, dy)
      const target = edge(end, -dx, -dy)
      const x1 = source.x + dx / length * gap
      const y1 = source.y + dy / length * gap
      const x2 = target.x - dx / length * gap
      const y2 = target.y - dy / length * gap
      make('line', { x1, y1, x2, y2, stroke: coral, 'stroke-width': 2 })
      const angle = Math.atan2(y2 - y1, x2 - x1)
      make('path', { d: `M ${x2} ${y2} L ${x2 - 9 * Math.cos(angle - 0.45)} ${y2 - 9 * Math.sin(angle - 0.45)} M ${x2} ${y2} L ${x2 - 9 * Math.cos(angle + 0.45)} ${y2 - 9 * Math.sin(angle + 0.45)}`, fill: 'none', stroke: coral, 'stroke-width': 2 })
    })

    document.body.append(svg)
    return { ok: true, errors: [] }
  }

  window.YubusCaptureAnnotations = { render, clear }
})(window)
