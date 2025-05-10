import subprocess
import json

def execute_commands(output_file):
    commands = [
        "sudo ovs-vsctl --format=json list port ovsp1",
        "sudo ovs-vsctl --format=json list port ovsp2",
        "sudo ovs-vsctl --format=json list port ovsp3",
        "sudo ovs-vsctl --format=json list port ovsp4",
        "sudo ovs-vsctl --format=json list port ovsp5",
        "sudo ovs-vsctl --format=json list port ovsp6",
        "sudo ovs-vsctl --format=json list port ovsp7",
        "sudo ovs-vsctl --format=json list port ovsp8",
        "sudo ovs-vsctl --format=json list port ovsp9",
        "sudo ovs-vsctl --format=json list port ovsp10",
        "sudo ovs-vsctl --format=json list port ovsp11",
        "sudo ovs-vsctl --format=json list port ovsp12",
        "sudo ovs-vsctl --format=json list bridge ovs-bridge1",
        "sudo ovs-vsctl --format=json list bridge ovs-bridge2"
    ]
    
    results = {}

    for command in commands:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            results[command] = {"error": result.stderr}
            continue
        
        try:
            data = json.loads(result.stdout)
            results[command] = data
        except json.JSONDecodeError:
            results[command] = {"error": "Ошибка при разборе JSON"}

    with open(output_file, 'w') as f:
        json.dump(results, f, indent=4)

if __name__ == "__main__":
    output_file = "command_results.json"
    execute_commands(output_file)
