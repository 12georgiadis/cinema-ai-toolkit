#!/usr/bin/env python3
"""
FCPXML Generator — Create valid FCPXML 1.11 timelines from structured JSON.

Usage:
    python fcpxml-generator.py --from-json structure.json --output timeline.fcpxml
    python fcpxml-generator.py --schema
"""

import argparse
import json
import sys
from dataclasses import dataclass, field
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom


@dataclass
class Marker:
    name: str
    offset_seconds: float
    marker_type: str = "chapter"  # chapter | todo | standard

    @property
    def offset_fcp(self) -> str:
        frames = int(self.offset_seconds * 24)
        return f"{frames}/24s"


@dataclass
class TitleClip:
    name: str
    duration_seconds: float
    text: str = ""
    markers: list[Marker] = field(default_factory=list)

    @property
    def duration_fcp(self) -> str:
        frames = int(self.duration_seconds * 24)
        return f"{frames}/24s"


@dataclass
class GapClip:
    name: str
    duration_seconds: float
    markers: list[Marker] = field(default_factory=list)

    @property
    def duration_fcp(self) -> str:
        frames = int(self.duration_seconds * 24)
        return f"{frames}/24s"


@dataclass
class TimelineProject:
    name: str
    fps: int = 24
    clips: list = field(default_factory=list)


def build_fcpxml(project: TimelineProject) -> str:
    """Build FCPXML 1.11 from a TimelineProject."""
    fcpxml = Element("fcpxml", version="1.11")

    # Resources
    resources = SubElement(fcpxml, "resources")
    SubElement(resources, "format", id="r1", name=f"FFVideoFormat1080p{project.fps}")
    SubElement(resources, "effect", id="r2", name="Basic Title", uid=".../Titles.localized/Bumper:Opener.localized/Basic Title.localized/Basic Title.moti")

    # Library > Event > Project
    library = SubElement(fcpxml, "library")
    event = SubElement(library, "event", name=project.name)
    proj = SubElement(event, "project", name=project.name)

    # Calculate total duration
    total_seconds = sum(c.duration_seconds for c in project.clips)
    total_frames = int(total_seconds * project.fps)
    sequence = SubElement(proj, "sequence", format="r1", duration=f"{total_frames}/{project.fps}s")

    spine = SubElement(sequence, "spine")

    for clip in project.clips:
        if isinstance(clip, TitleClip):
            title_el = SubElement(spine, "title",
                                  ref="r2",
                                  name=clip.name,
                                  duration=clip.duration_fcp)
            text_el = SubElement(title_el, "text")
            text_style = SubElement(text_el, "text-style", ref="ts1")
            text_style.text = clip.text or clip.name

            for marker in clip.markers:
                attrs = {"start": marker.offset_fcp, "value": marker.name}
                if marker.marker_type == "chapter":
                    SubElement(title_el, "chapter-marker", **attrs)
                elif marker.marker_type == "todo":
                    SubElement(title_el, "marker", start=marker.offset_fcp, value=marker.name, completed="0")
                else:
                    SubElement(title_el, "marker", **attrs)

        elif isinstance(clip, GapClip):
            gap_el = SubElement(spine, "gap",
                                name=clip.name,
                                duration=clip.duration_fcp)
            for marker in clip.markers:
                SubElement(gap_el, "chapter-marker",
                           start=marker.offset_fcp,
                           value=marker.name)

    # Pretty print
    rough = tostring(fcpxml, encoding="unicode")
    dom = minidom.parseString(rough)
    pretty = dom.toprettyxml(indent="  ", encoding=None)
    # Remove extra XML declaration, add DOCTYPE
    lines = pretty.split("\n")
    lines = [l for l in lines if not l.startswith("<?xml")]
    output = '<?xml version="1.0" encoding="UTF-8"?>\n'
    output += '<!DOCTYPE fcpxml>\n'
    output += "\n".join(lines).strip()
    return output


def from_json(filepath: str) -> TimelineProject:
    """Load a TimelineProject from JSON."""
    with open(filepath) as f:
        data = json.load(f)

    project = TimelineProject(
        name=data.get("project_name", "Untitled"),
        fps=data.get("fps", 24)
    )

    for seq in data.get("sequences", []):
        markers = [
            Marker(
                name=m["name"],
                offset_seconds=m.get("offset_seconds", 0),
                marker_type=m.get("type", "chapter")
            )
            for m in seq.get("markers", [])
        ]

        if seq.get("type") == "title":
            project.clips.append(TitleClip(
                name=seq["title"],
                duration_seconds=seq.get("duration_seconds", 60),
                text=seq.get("text", seq["title"]),
                markers=markers
            ))
        else:
            project.clips.append(GapClip(
                name=seq["title"],
                duration_seconds=seq.get("duration_seconds", 60),
                markers=markers
            ))

    return project


SCHEMA = {
    "project_name": "My Film",
    "fps": 24,
    "sequences": [
        {
            "title": "Act 1 — Opening",
            "type": "title",
            "duration_seconds": 120,
            "text": "ACT ONE",
            "markers": [
                {"name": "Key moment", "offset_seconds": 30, "type": "chapter"}
            ]
        },
        {
            "title": "Interview placeholder",
            "type": "gap",
            "duration_seconds": 300,
            "markers": [
                {"name": "Important beat", "offset_seconds": 60, "type": "todo"}
            ]
        }
    ]
}


def main():
    parser = argparse.ArgumentParser(description="Generate FCPXML 1.11 timelines from JSON")
    parser.add_argument("--from-json", help="Input JSON file path")
    parser.add_argument("--output", "-o", default="output.fcpxml", help="Output FCPXML file path")
    parser.add_argument("--schema", action="store_true", help="Print expected JSON schema")
    args = parser.parse_args()

    if args.schema:
        print(json.dumps(SCHEMA, indent=2))
        return

    if not args.from_json:
        parser.print_help()
        sys.exit(1)

    project = from_json(args.from_json)
    xml_output = build_fcpxml(project)

    with open(args.output, "w") as f:
        f.write(xml_output)

    clip_count = len(project.clips)
    marker_count = sum(len(c.markers) for c in project.clips)
    print(f"Generated {args.output}: {clip_count} clips, {marker_count} markers")


if __name__ == "__main__":
    main()
