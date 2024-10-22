document.addEventListener('DOMContentLoaded', function() {
    const data = [50, 70, 30, 90, 160]; // Dữ liệu đầu vào, giá trị phần trăm
    const chartContainer = document.getElementById('chartContainer');

    data.forEach(value => {
        const bar = document.createElement('div');
        bar.className = 'chart-bar';
        bar.style.height = `${value}%`;

        const label = document.createElement('span');
        label.className = 'label';
        label.textContent = `${value}%`;

        bar.appendChild(label);
        chartContainer.appendChild(bar);
    });
});
