#include <iostream>
#include <vector>

using namespace std;

struct Process {
    int id; // ID của tiến trình
    int burstTime; // Thời gian thực hiện tiến trình
    int waitingTime; // Thời gian chờ
    int completionTime; // Thời gian hoàn thành
};

void findWaitingTime(vector<Process>& processes) {
    processes[0].waitingTime = 0; // Tiến trình đầu tiên không cần chờ

    // Tính thời gian chờ cho các tiến trình còn lại
    for (size_t i = 1; i < processes.size(); i++) {
        processes[i].waitingTime = processes[i - 1].completionTime;
    }
}

void findCompletionTime(vector<Process>& processes) {
    processes[0].completionTime = processes[0].burstTime;

    // Tính thời gian hoàn thành cho từng tiến trình
    for (size_t i = 1; i < processes.size(); i++) {
        processes[i].completionTime = processes[i - 1].completionTime + processes[i].burstTime;
    }
}

void displayProcesses(const vector<Process>& processes) {
    cout << "ID\tBurst Time\tWaiting Time\tCompletion Time\n";
    for (const auto& process : processes) {
        cout << process.id << "\t" << process.burstTime << "\t\t" << process.waitingTime << "\t\t" << process.completionTime << "\n";
    }
}

int main() {
    vector<Process> processes = {
        {1, 5, 0, 0}, // {ID, Burst Time, Waiting Time, Completion Time}
        {2, 3, 0, 0},
        {3, 8, 0, 0},
        {4, 6, 0, 0}
    };

    // Tính thời gian hoàn thành cho mỗi tiến trình
    findCompletionTime(processes);

    // Tính thời gian chờ dựa trên thời gian hoàn thành
    findWaitingTime(processes);

    // Hiển thị kết quả
    displayProcesses(processes);

    return 0;
}
