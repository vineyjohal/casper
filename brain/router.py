import importlib

def execute_skill(intent, user_input):
    try:
        skill_module = importlib.import_module(f"skills.{intent}")
        if hasattr(skill_module, "run"):
            response = skill_module.run(user_input)
            print("🧠 Casper:", response)
        else:
            print(f"⚠️ Skill '{intent}' has no 'run()' function.")
    except ModuleNotFoundError:
        print(f"❌ Skill '{intent}' not found.")
    except Exception as e:
        print(f"💥 Error running skill '{intent}': {e}")