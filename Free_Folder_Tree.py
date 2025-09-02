#!/usr/bin/env python3
"""
Free Professional Folder Tree Generator
AI Development Carousel: v0 Enhanced

Creates professional folder tree visualizations in multiple formats
Supports txt, png, svg, pdf outputs with configurable styles and depth

(c) 2024-2025 Hans Hendrickx MD PhD and Karl Hendrickx MSc - MIT License
In cooperation with v0 AI Assistant

Usage:
    Simple:     python Free_Folder_Tree.py /path/to/project
    Beautiful:  python Free_Folder_Tree.py . --style artisanal --icons
    Perfect:    python Free_Folder_Tree.py . --style artisanal --icons --max-files 5 --depth 3
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Try to import optional dependencies for advanced features
try:
    from PIL import Image, ImageDraw, ImageFont

    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import svgwrite

    SVG_AVAILABLE = True
except ImportError:
    SVG_AVAILABLE = False

try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4

    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False


class FolderTreeGenerator:
    """Professional folder tree generator with multiple output formats"""

    def __init__(self):
        self.icons = {
            "folder": "📁",
            "file": "📄",
            "python": "🐍",
            "javascript": "📜",
            "html": "🌐",
            "css": "🎨",
            "image": "🖼️",
            "document": "📋",
            "archive": "📦",
            "config": "⚙️",
            "database": "🗄️",
            "executable": "⚡",
        }

        self.tree_chars = {
            "simple": {
                "branch": "├── ",
                "last": "└── ",
                "pipe": "│   ",
                "space": "    ",
            },
            "artisanal": {
                "branch": "├─ ",
                "last": "└─ ",
                "pipe": "│  ",
                "space": "   ",
            },
            "minimal": {"branch": "+ ", "last": "+ ", "pipe": "| ", "space": "  "},
        }

        self.output_dir = Path.home() / "tools" / "Free_Folder_Tree" / "Output"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def get_file_icon(self, file_path: Path) -> str:
        """Get appropriate icon for file type"""
        if file_path.is_dir():
            return self.icons["folder"]

        suffix = file_path.suffix.lower()
        icon_map = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "javascript",
            ".jsx": "javascript",
            ".tsx": "javascript",
            ".html": "html",
            ".htm": "html",
            ".css": "css",
            ".scss": "css",
            ".sass": "css",
            ".png": "image",
            ".jpg": "image",
            ".jpeg": "image",
            ".gif": "image",
            ".svg": "image",
            ".pdf": "document",
            ".doc": "document",
            ".docx": "document",
            ".txt": "document",
            ".zip": "archive",
            ".tar": "archive",
            ".gz": "archive",
            ".rar": "archive",
            ".json": "config",
            ".yaml": "config",
            ".yml": "config",
            ".toml": "config",
            ".db": "database",
            ".sqlite": "database",
            ".sql": "database",
            ".exe": "executable",
            ".bat": "executable",
            ".sh": "executable",
        }

        return self.icons.get(icon_map.get(suffix, "file"), self.icons["file"])

    def get_file_size(self, file_path: Path) -> str:
        """Get human-readable file size"""
        try:
            size = file_path.stat().st_size
            for unit in ["B", "KB", "MB", "GB"]:
                if size < 1024:
                    return f"{size:.1f}{unit}"
                size /= 1024
            return f"{size:.1f}TB"
        except Exception:
            return ""

    def should_exclude(self, path: Path, exclude_patterns: List[str]) -> bool:
        """Check if path should be excluded based on patterns"""
        name = path.name
        for pattern in exclude_patterns:
            if pattern in name or name.startswith(pattern):
                return True
        return False

    def generate_tree_structure(
        self,
        root_path: Path,
        max_depth: int = 2,
        max_files: Optional[int] = None,
        show_hidden: bool = False,
        show_sizes: bool = False,
        exclude_patterns: Optional[List[str]] = None,
        style: str = "simple",
        use_icons: bool = False,
    ) -> Tuple[List[str], Dict]:
        """Generate tree structure with comprehensive options"""

        if exclude_patterns is None:
            exclude_patterns = [
                ".git",
                "__pycache__",
                "node_modules",
                ".vscode",
                ".idea",
            ]

        chars = self.tree_chars.get(style, self.tree_chars["simple"])
        lines = []
        stats = {"folders": 0, "files": 0, "total_size": 0}

        def traverse(
            path: Path, prefix: str = "", depth: int = 0, is_last: bool = True
        ):
            if depth > max_depth:
                return

            try:
                if not show_hidden and path.name.startswith("."):
                    return

                if self.should_exclude(path, exclude_patterns):
                    return

                # Build line
                connector = chars["last"] if is_last else chars["branch"]
                icon = self.get_file_icon(path) if use_icons else ""
                size_info = (
                    f" ({self.get_file_size(path)})"
                    if show_sizes and path.is_file()
                    else ""
                )

                line = f"{prefix}{connector}{icon}{path.name}{size_info}"
                lines.append(line)

                # Update stats
                if path.is_dir():
                    stats["folders"] += 1
                else:
                    stats["files"] += 1
                    try:
                        stats["total_size"] += path.stat().st_size
                    except Exception:
                        pass

                # Recurse into directories
                if path.is_dir() and depth < max_depth:
                    try:
                        children = sorted(
                            path.iterdir(), key=lambda x: (x.is_file(), x.name.lower())
                        )

                        if not show_hidden:
                            children = [
                                c for c in children if not c.name.startswith(".")
                            ]

                        children = [
                            c
                            for c in children
                            if not self.should_exclude(c, exclude_patterns)
                        ]

                        if max_files and len(children) > max_files:
                            children = children[:max_files]
                            truncated_line = f"{prefix}{chars['space']}{chars['last']}... ({len(list(path.iterdir())) - max_files} more items)"
                            children.append(None)  # Placeholder for truncation message

                        for i, child in enumerate(children):
                            if child is None:  # Truncation message
                                lines.append(truncated_line)
                                continue

                            child_is_last = i == len(children) - 1
                            child_prefix = prefix + (
                                chars["space"] if is_last else chars["pipe"]
                            )
                            traverse(child, child_prefix, depth + 1, child_is_last)

                    except PermissionError:
                        lines.append(
                            f"{prefix}{chars['space']}{chars['last']}[Permission Denied]"
                        )
                    except Exception as e:
                        lines.append(
                            f"{prefix}{chars['space']}{chars['last']}[Error: {str(e)[:50]}]"
                        )

            except Exception as e:
                lines.append(
                    f"{prefix}{chars['last']}[Error accessing {path.name}: {str(e)[:30]}]"
                )

        # Start traversal
        root_line = (
            f"{self.get_file_icon(root_path) if use_icons else ''}{root_path.name}/"
        )
        lines.append(root_line)
        stats["folders"] += 1

        try:
            children = sorted(
                root_path.iterdir(), key=lambda x: (x.is_file(), x.name.lower())
            )
            if not show_hidden:
                children = [c for c in children if not c.name.startswith(".")]
            children = [
                c for c in children if not self.should_exclude(c, exclude_patterns)
            ]

            if max_files and len(children) > max_files:
                children = children[:max_files]

            for i, child in enumerate(children):
                is_last = i == len(children) - 1
                traverse(child, "", 1, is_last)

        except PermissionError:
            lines.append("[Permission Denied]")
        except Exception as e:
            lines.append(f"[Error: {e}]")

        return lines, stats

    def save_text_output(
        self, lines: List[str], stats: Dict, output_path: Path, root_path: Path
    ):
        """Save tree as text file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("=" * 80 + "\n")
            f.write("FREE PROFESSIONAL FOLDER TREE\n")
            f.write("AI Development Carousel: v0 Enhanced\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Generated: {timestamp}\n")
            f.write(f"Root Path: {root_path.absolute()}\n")
            f.write(f"Statistics: {stats['folders']} folders, {stats['files']} files\n")
            if stats["total_size"] > 0:
                total_size = stats["total_size"]
                for unit in ["B", "KB", "MB", "GB"]:
                    if total_size < 1024:
                        f.write(f"Total Size: {total_size:.1f}{unit}\n")
                        break
                    total_size /= 1024
            f.write("\n" + "-" * 80 + "\n\n")

            for line in lines:
                f.write(line + "\n")

            f.write("\n" + "=" * 80 + "\n")
            f.write("Generated by Free_Folder_Tree.py\n")
            f.write("(c) 2024-2025 Hans Hendrickx MD PhD and Karl Hendrickx MSc\n")

    def save_png_output(
        self, lines: List[str], stats: Dict, output_path: Path, root_path: Path
    ):
        """Save tree as PNG image"""
        if not PIL_AVAILABLE:
            print(
                "✗ PNG generation failed: PIL not available. Install with: pip install Pillow"
            )
            return

        print(f"[PNG] Starting generation for {len(lines)} lines")
        print(f"[PNG] Output path: {output_path}")

        try:
            # Calculate image dimensions with padding
            line_height = 18
            char_width = 8
            padding = 40
            max_line_length = max(len(line) for line in lines) if lines else 50
            width = max_line_length * char_width + padding * 2
            height = len(lines) * line_height + 150

            print(f"[PNG] Image dimensions: {width}x{height}")

            # Create image with white background
            img = Image.new("RGB", (width, height), color="white")
            draw = ImageDraw.Draw(img)
            print("[PNG] Image canvas created")

            # Use default font - more reliable than TrueType
            try:
                font = ImageFont.load_default()
                print("[PNG] Using default font")
            except Exception as e:
                print(f"[PNG] Font loading failed: {e}")
                font = None

            # Draw header
            y_pos = 20
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            header_lines = [
                "FREE PROFESSIONAL FOLDER TREE",
                f"Generated: {timestamp}",
                f"Root: {root_path.name}",
                f"Stats: {stats['folders']} folders, {stats['files']} files",
                "-" * 50,
            ]

            print(f"[PNG] Drawing header ({len(header_lines)} lines)")
            for header_line in header_lines:
                if font:
                    draw.text((padding, y_pos), header_line, fill="black", font=font)
                y_pos += line_height

            y_pos += 10  # Extra spacing

            # Draw tree lines
            print(f"[PNG] Drawing tree structure ({len(lines)} lines)")
            for i, line in enumerate(lines):
                if font:
                    # Truncate very long lines to fit
                    display_line = line[:120] if len(line) > 120 else line
                    draw.text((padding, y_pos), display_line, fill="black", font=font)
                y_pos += line_height

                # Progress feedback for large trees
                if i > 0 and i % 50 == 0:
                    print(f"[PNG] Progress: {i}/{len(lines)} lines drawn")

            print(f"[PNG] All content drawn, saving to: {output_path}")

            # Save the image
            img.save(str(output_path), "PNG")
            print("[PNG] File saved successfully")

            # Verify file creation
            if output_path.exists():
                file_size = output_path.stat().st_size
                print(f"[PNG] ✓ Verification successful: {file_size:,} bytes")
                return True
            else:
                print("[PNG] ✗ ERROR: File not found after save attempt")
                return False

        except Exception as e:
            print(f"[PNG] ✗ CRITICAL ERROR: {e}")
            print(f"[PNG] Exception type: {type(e).__name__}")
            import traceback

            print("[PNG] Full traceback:")
            traceback.print_exc()
            return False

    def save_svg_output(
        self, lines: List[str], stats: Dict, output_path: Path, root_path: Path
    ):
        """Save tree as SVG"""
        if not SVG_AVAILABLE:
            print("Warning: svgwrite not available. Install with: pip install svgwrite")
            return

        line_height = 20
        char_width = 8
        width = max(len(line) for line in lines) * char_width + 100
        height = len(lines) * line_height + 200

        dwg = svgwrite.Drawing(str(output_path), size=(width, height))

        # Add styles
        dwg.defs.add(
            dwg.style(
                """
            .header { font-family: Arial, sans-serif; font-size: 16px; font-weight: bold; }
            .info { font-family: Arial, sans-serif; font-size: 12px; fill: gray; }
            .tree { font-family: 'Courier New', monospace; font-size: 14px; }
        """
            )
        )

        # Add header
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dwg.add(
            dwg.text("FREE PROFESSIONAL FOLDER TREE", insert=(20, 30), class_="header")
        )
        dwg.add(dwg.text(f"Generated: {timestamp}", insert=(20, 50), class_="info"))
        dwg.add(dwg.text(f"Root: {root_path.name}", insert=(20, 70), class_="info"))
        dwg.add(
            dwg.text(
                f"Stats: {stats['folders']} folders, {stats['files']} files",
                insert=(20, 90),
                class_="info",
            )
        )

        # Add tree
        y_offset = 120
        for line in lines:
            dwg.add(dwg.text(line, insert=(20, y_offset), class_="tree"))
            y_offset += line_height

        dwg.save()

    def save_pdf_output(
        self, lines: List[str], stats: Dict, output_path: Path, root_path: Path
    ):
        """Save tree as PDF"""
        if not PDF_AVAILABLE:
            print(
                "Warning: reportlab not available. Install with: pip install reportlab"
            )
            return

        c = canvas.Canvas(str(output_path), pagesize=A4)
        width, height = A4

        # Header
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, "FREE PROFESSIONAL FOLDER TREE")

        c.setFont("Helvetica", 10)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.drawString(50, height - 70, f"Generated: {timestamp}")
        c.drawString(50, height - 85, f"Root: {str(root_path)}")
        c.drawString(
            50,
            height - 100,
            f"Statistics: {stats['folders']} folders, {stats['files']} files",
        )

        # Tree content
        c.setFont("Courier", 9)
        y_position = height - 130

        for line in lines:
            if y_position < 50:  # New page
                c.showPage()
                y_position = height - 50

            c.drawString(50, y_position, line[:100])  # Limit line length
            y_position -= 12

        c.save()

    def generate_and_save(self, root_path: str, **kwargs):
        """Main method to generate and save folder tree"""
        path = Path(root_path).resolve()

        if not path.exists():
            print(f"Error: Path '{root_path}' does not exist")
            return

        if not path.is_dir():
            print(f"Error: Path '{root_path}' is not a directory")
            return

        print(f"Generating folder tree for: {path}")
        print(f"Output directory: {self.output_dir}")

        formats = kwargs.pop("formats", ["txt"])

        print(f"Requested formats: {formats}")
        print(
            f"Library availability: PIL={PIL_AVAILABLE}, SVG={SVG_AVAILABLE}, PDF={PDF_AVAILABLE}"
        )

        # Generate tree structure
        lines, stats = self.generate_tree_structure(path, **kwargs)

        # Create timestamp for filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"folder_tree_{path.name}_{timestamp}"

        print(f"[DEBUG] About to process formats: {formats}")
        print(f"[DEBUG] Base filename: {base_name}")

        # Save in different formats
        if "txt" in formats:
            print("[DEBUG] Processing TXT format...")
            txt_path = self.output_dir / f"{base_name}.txt"
            self.save_text_output(lines, stats, txt_path, path)
            print(f"✓ Text saved: {txt_path}")

        if "png" in formats:
            print("[DEBUG] Processing PNG format...")
            print(f"[DEBUG] PNG format requested, PIL_AVAILABLE={PIL_AVAILABLE}")
            if PIL_AVAILABLE:
                png_path = self.output_dir / f"{base_name}.png"
                print(f"[DEBUG] PNG path created: {png_path}")
                print("[DEBUG] About to call save_png_output...")
                try:
                    self.save_png_output(lines, stats, png_path, path)
                    print("[DEBUG] save_png_output completed")
                    print(f"✓ PNG saved: {png_path}")
                except Exception as e:
                    print(f"[ERROR] Exception in save_png_output: {e}")
                    import traceback

                    traceback.print_exc()
            else:
                print(
                    "✗ PNG skipped: PIL not available. Install with: pip install Pillow"
                )

        if "svg" in formats:
            print("[DEBUG] Processing SVG format...")
            print(f"[DEBUG] SVG format requested, SVG_AVAILABLE={SVG_AVAILABLE}")
            if SVG_AVAILABLE:
                svg_path = self.output_dir / f"{base_name}.svg"
                self.save_svg_output(lines, stats, svg_path, path)
                print(f"✓ SVG saved: {svg_path}")
            else:
                print(
                    "✗ SVG skipped: svgwrite not available. Install with: pip install svgwrite"
                )

        if "pdf" in formats:
            print("[DEBUG] Processing PDF format...")
            print(f"[DEBUG] PDF format requested, PDF_AVAILABLE={PDF_AVAILABLE}")
            if PDF_AVAILABLE:
                pdf_path = self.output_dir / f"{base_name}.pdf"
                self.save_pdf_output(lines, stats, pdf_path, path)
                print(f"✓ PDF saved: {pdf_path}")
            else:
                print(
                    "✗ PDF skipped: reportlab not available. Install with: pip install reportlab"
                )

        print("[DEBUG] Format processing completed")

        # Display preview
        print("\n" + "=" * 60)
        print("PREVIEW:")
        print("=" * 60)
        for i, line in enumerate(lines[:20]):  # Show first 20 lines
            print(line)
        if len(lines) > 20:
            print(f"... and {len(lines) - 20} more lines")

        print(f"\nStatistics: {stats['folders']} folders, {stats['files']} files")

        return lines, stats


def main():
    parser = argparse.ArgumentParser(
        description="Free Professional Folder Tree Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Simple:     python Free_Folder_Tree.py /path/to/project
  Simple:     python Free_Folder_Tree.py . 2
  Simple:     python Free_Folder_Tree.py . 3 beautiful
  Beautiful:  python Free_Folder_Tree.py . --style artisanal --icons
  Perfect:    python Free_Folder_Tree.py . --style artisanal --icons --max-files 5 --depth 3 --formats txt,png,svg

Complexity Levels:
  Basic:      Default settings, text output only
  Beautiful:  Artisanal style with icons, multiple formats
  Perfect:    All features enabled, professional output

View Output:
  Windows:    explorer C:\\Users\\%USERNAME%\\tools\\Free_Folder_Tree\\Output
  Unix:       open ~/tools/Free_Folder_Tree/Output
        """,
    )

    parser.add_argument(
        "path",
        help="Directory path to generate tree for (use quotes for paths with spaces)",
    )
    parser.add_argument(
        "depth_pos", nargs="?", type=int, help="Depth (1-5) - positional argument"
    )
    parser.add_argument(
        "style_pos",
        nargs="?",
        choices=["simple", "beautiful", "artisanal", "minimal"],
        help="Style - positional argument (beautiful=artisanal+icons)",
    )

    parser.add_argument(
        "--depth",
        type=int,
        default=2,
        choices=range(1, 6),
        help="Maximum depth (1-5, default: 2)",
    )
    parser.add_argument("--max-files", type=int, help="Maximum files per directory")
    parser.add_argument(
        "--style",
        choices=["simple", "artisanal", "minimal"],
        default="simple",
        help="Tree drawing style",
    )
    parser.add_argument("--icons", action="store_true", help="Use file type icons")
    parser.add_argument("--hidden", action="store_true", help="Show hidden files")
    parser.add_argument("--sizes", action="store_true", help="Show file sizes")
    parser.add_argument(
        "--formats",
        type=str,
        default="txt",
        help='Output formats: comma-separated "txt,png,svg,pdf" or space-separated "txt png svg pdf" (default: txt)',
    )
    parser.add_argument(
        "--exclude",
        nargs="+",
        default=[".git", "__pycache__", "node_modules"],
        help="Patterns to exclude",
    )

    args = parser.parse_args()

    if isinstance(args.formats, str):
        if "," in args.formats:
            args.formats = [f.strip() for f in args.formats.split(",")]
        else:
            args.formats = args.formats.split()

    valid_formats = ["txt", "png", "svg", "pdf"]
    invalid_formats = [f for f in args.formats if f not in valid_formats]
    if invalid_formats:
        print(f"Warning: Invalid formats ignored: {invalid_formats}")
        print(f"Valid formats are: {', '.join(valid_formats)}")

    args.formats = [f for f in args.formats if f in valid_formats]
    if not args.formats:
        args.formats = ["txt"]  # Default fallback

    if args.depth_pos is not None:
        args.depth = max(1, min(5, args.depth_pos))  # Clamp to valid range

    if args.style_pos is not None:
        if args.style_pos == "beautiful":
            args.style = "artisanal"
            args.icons = True
            args.formats = ["txt", "png"] if PIL_AVAILABLE else ["txt"]
        else:
            args.style = args.style_pos

    # Create generator and run
    generator = FolderTreeGenerator()

    try:
        generator.generate_and_save(
            root_path=args.path,
            max_depth=args.depth,
            max_files=args.max_files,
            show_hidden=args.hidden,
            show_sizes=args.sizes,
            exclude_patterns=args.exclude,
            style=args.style,
            use_icons=args.icons,
            formats=args.formats,
        )

        print("\n✓ Generation complete! Check output directory:")
        print(f"  {generator.output_dir}")
        print("\nTo view output files:")
        print(f'  Windows: explorer "{generator.output_dir}"')
        print(f'  Unix:    open "{generator.output_dir}"')

    except KeyboardInterrupt:
        print("\n⚠ Generation cancelled by user")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
