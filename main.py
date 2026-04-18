#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.progress import Progress
from modules import (
    phone_lookup, email_lookup, domain_lookup, username_lookup,
    ReportGenerator, display_table
)
from config import REPORT_FORMAT

console = Console()

def print_banner():
    banner = """
    ╔═══════════════════════════════════════════╗
    ║     Advanced OSINT Toolkit v2.0           ║
    ║     Intelligence Gathering Framework      ║
    ╚═══════════════════════════════════════════╝
    """
    console.print(banner, style="bold blue")

def save_report(data: dict, target: str, module_name: str):
    """حفظ التقرير"""
    if Confirm.ask("💾 هل تريد حفظ التقرير؟"):
        format_choice = Prompt.ask(
            "اختر صيغة التقرير",
            choices=["txt", "json", "html"],
            default=REPORT_FORMAT
        )
        
        generator = ReportGenerator(report_type=format_choice)
        generator.add_section(f"{module_name.upper()} Results", data)
        
        filename = f"{module_name}_{target.replace('@', '_').replace('.', '_')}"
        filepath = generator.save(filename)
        console.print(f"[green]✅ تم حفظ التقرير في: {filepath}[/green]")

def interactive_mode():
    """الوضع التفاعلي"""
    print_banner()
    
    while True:
        console.print("\n[bold cyan]اختر نوع البحث:[/bold cyan]")
        console.print("1. 📱 رقم هاتف")
        console.print("2. 📧 بريد إلكتروني")
        console.print("3. 🌐 نطاق (Domain)")
        console.print("4. 👤 اسم مستخدم")
        console.print("5. 🚪 خروج")
        
        choice = Prompt.ask("الخيار", choices=["1", "2", "3", "4", "5"])
        
        if choice == "5":
            console.print("[yellow]👋 مع السلامة![/yellow]")
            break
        
        target = Prompt.ask("🔍 أدخل الهدف")
        
        with Progress() as progress:
            task = progress.add_task("[cyan]جاري البحث...", total=None)
            
            try:
                if choice == "1":
                    result = phone_lookup(target)
                    module_name = "phone"
                elif choice == "2":
                    result = email_lookup(target)
                    module_name = "email"
                elif choice == "3":
                    result = domain_lookup(target)
                    module_name = "domain"
                elif choice == "4":
                    result = username_lookup(target)
                    module_name = "username"
                
                progress.update(task, completed=True)
                
                if "error" in result:
                    console.print(f"[red]❌ خطأ: {result['error']}[/red]")
                else:
                    # عرض النتائج
                    if module_name == "username":
                        console.print(Panel(f"تم العثور على {result['platforms_found']} حساب", style="green"))
                        for profile in result['profiles']:
                            console.print(f"  • {profile['platform']}: {profile['url']}")
                    else:
                        # تحويل النتائج المتداخلة إلى عرض مناسب
                        flat_result = {}
                        for key, value in result.items():
                            if isinstance(value, dict):
                                for subkey, subvalue in value.items():
                                    flat_result[f"{key}.{subkey}"] = subvalue
                            elif isinstance(value, list) and value:
                                flat_result[key] = ", ".join(str(v) for v in value[:5])
                            else:
                                flat_result[key] = value
                        
                        display_table(f"نتائج {module_name}", flat_result)
                    
                    save_report(result, target, module_name)
                    
            except Exception as e:
                progress.update(task, completed=True)
                console.print(f"[red]❌ حدث خطأ غير متوقع: {str(e)}[/red]")

def main():
    parser = argparse.ArgumentParser(
        description="Advanced OSINT Toolkit - أداة متقدمة لجمع المعلومات الاستخباراتية",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
أمثلة:
  python main.py -p +201234567890
  python main.py -e user@example.com
  python main.py -d example.com
  python main.py -u username
  python main.py -i  (للوضع التفاعلي)
        """
    )
    
    parser.add_argument("-p", "--phone", help="رقم هاتف للبحث")
    parser.add_argument("-e", "--email", help="بريد إلكتروني للبحث")
    parser.add_argument("-d", "--domain", help="نطاق للبحث")
    parser.add_argument("-u", "--username", help="اسم مستخدم للبحث")
    parser.add_argument("-i", "--interactive", action="store_true", help="الوضع التفاعلي")
    parser.add_argument("-o", "--output", help="حفظ التقرير مباشرة (بدون سؤال)")
    
    args = parser.parse_args()
    
    # إذا لم يتم تمرير أي وسيط، اذهب للوضع التفاعلي
    if len(sys.argv) == 1:
        interactive_mode()
        return
    
    if args.interactive:
        interactive_mode()
        return
    
    print_banner()
    
    result = None
    module_name = ""
    target = ""
    
    with Progress() as progress:
        task = progress.add_task("[cyan]جاري المعالجة...", total=None)
        
        try:
            if args.phone:
                result = phone_lookup(args.phone)
                module_name = "phone"
                target = args.phone
            elif args.email:
                result = email_lookup(args.email)
                module_name = "email"
                target = args.email
            elif args.domain:
                result = domain_lookup(args.domain)
                module_name = "domain"
                target = args.domain
            elif args.username:
                result = username_lookup(args.username)
                module_name = "username"
                target = args.username
            else:
                console.print("[red]❌ الرجاء تحديد هدف للبحث[/red]")
                parser.print_help()
                return
            
            progress.update(task, completed=True)
            
            if "error" in result:
                console.print(f"[red]❌ خطأ: {result['error']}[/red]")
                return
            
            # عرض النتائج
            if module_name == "username":
                console.print(Panel(f"تم العثور على {result['platforms_found']} حساب", style="green"))
                for profile in result['profiles']:
                    console.print(f"  • {profile['platform']}: {profile['url']}")
            else:
                flat_result = {}
                for key, value in result.items():
                    if isinstance(value, dict):
                        for subkey, subvalue in value.items():
                            flat_result[f"{key}.{subkey}"] = subvalue
                    elif isinstance(value, list) and value:
                        flat_result[key] = ", ".join(str(v) for v in value[:5])
                    else:
                        flat_result[key] = value
                
                display_table(f"نتائج {module_name}", flat_result)
            
            # حفظ التقرير
            if args.output:
                generator = ReportGenerator(report_type=REPORT_FORMAT)
                generator.add_section(f"{module_name.upper()} Results", result)
                filepath = generator.save(args.output)
                console.print(f"[green]✅ تم حفظ التقرير في: {filepath}[/green]")
            else:
                save_report(result, target, module_name)
                
        except KeyboardInterrupt:
            console.print("\n[yellow]⚠️ تم إلغاء العملية[/yellow]")
        except Exception as e:
            progress.update(task, completed=True)
            console.print(f"[red]❌ حدث خطأ غير متوقع: {str(e)}[/red]")

if __name__ == "__main__":
    main()
