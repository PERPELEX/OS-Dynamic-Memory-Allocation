let memoryBlocks = [
    { size: 2, occupied: false },
    { size: 120, occupied: true },
    { size: 20, occupied: false },
    { size: 150, occupied: true },
    { size: 160, occupied: false },
    { size: 1, occupied: true },
    { size: 4, occupied: false },
    { size: 554, occupied: true },
    { size: 124, occupied: false }
];

function displayMemory() {
    const container = document.getElementById('memory-container');
    container.innerHTML = '';
    memoryBlocks.forEach((block, index) => {
        const div = document.createElement('div');
        div.classList.add('memory-block');
        div.classList.add(block.occupied ? 'occupied' : 'free');
        const fragmentation = block.occupied ? block.size - block.allocatedSize : 0;
        div.innerText = `Block #${index + 1}: ${block.size}KB (${block.occupied ? 'Occupied' : 'Free'}), Internal Fragmentation: ${fragmentation}KB`;
        div.onclick = () => toggleSelection(index);
        div.dataset.index = index;
        container.appendChild(div);
    });
}

function allocateMemory() {
    const requestSize = parseInt(document.getElementById('request-size').value);
    for (let i = 0; i < memoryBlocks.length; i++) {
        if (!memoryBlocks[i].occupied && memoryBlocks[i].size >= requestSize) {
            memoryBlocks[i].occupied = true;
            memoryBlocks[i].allocatedSize = requestSize;
            break;
        }
    }
    displayMemory();
}

function allocateMemoryBestFit() {
    const requestSize = parseInt(document.getElementById('request-size').value);
    let bestFitIndex = -1;
    let bestFitSize = Number.MAX_SAFE_INTEGER;

    for (let i = 0; i < memoryBlocks.length; i++) {
        if (!memoryBlocks[i].occupied && memoryBlocks[i].size >= requestSize && memoryBlocks[i].size < bestFitSize) {
            bestFitIndex = i;
            bestFitSize = memoryBlocks[i].size;
        }
    }

    if (bestFitIndex !== -1) {
        memoryBlocks[bestFitIndex].occupied = true;
        memoryBlocks[bestFitIndex].allocatedSize = requestSize;
    }

    displayMemory();
}

function allocateMemoryWorstFit() {
    const requestSize = parseInt(document.getElementById('request-size').value);
    let worstFitIndex = -1;
    let worstFitSize = 0;

    for (let i = 0; i < memoryBlocks.length; i++) {
        if (!memoryBlocks[i].occupied && memoryBlocks[i].size >= requestSize && memoryBlocks[i].size > worstFitSize) {
            worstFitIndex = i;
            worstFitSize = memoryBlocks[i].size;
        }
    }

    if (worstFitIndex !== -1) {
        memoryBlocks[worstFitIndex].occupied = true;
        memoryBlocks[worstFitIndex].allocatedSize = requestSize;
    }

    displayMemory();
}

function deallocateMemory() {
    const requestSize = parseInt(document.getElementById('request-size').value);
    for (let i = 0; i < memoryBlocks.length; i++) {
        if (memoryBlocks[i].occupied && memoryBlocks[i].size === requestSize) {
            memoryBlocks[i].occupied = false;
            break;
        }
    }
    displayMemory();
}

function resetMemory() {
    memoryBlocks = [
        { size: 2, occupied: false },
        { size: 120, occupied: true },
        { size: 20, occupied: false },
        { size: 150, occupied: true },
        { size: 160, occupied: false },
        { size: 1, occupied: true },
        { size: 4, occupied: false },
        { size: 554, occupied: true },
        { size: 124, occupied: false }
    ];
    displayMemory();
}

function toggleSelection(index) {
    const blockDiv = document.querySelector(`.memory-block[data-index='${index}']`);
    blockDiv.classList.toggle('selected');
}

window.onload = displayMemory;
