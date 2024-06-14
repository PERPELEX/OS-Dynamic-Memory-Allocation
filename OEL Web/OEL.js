class MemoryBlock {
    constructor(size, isOccupied = false) {
        this.size = size;
        this.isOccupied = isOccupied;
    }
}

class MemoryAllocator {
    constructor() {
        // Initialize memory blocks
        this.memoryBlocks = [
            new MemoryBlock(2), new MemoryBlock(120), new MemoryBlock(20),
            new MemoryBlock(150), new MemoryBlock(160), new MemoryBlock(1),
            new MemoryBlock(4), new MemoryBlock(554), new MemoryBlock(124)
        ];
    }

    allocate(requestSize) {
        for (let block of this.memoryBlocks) {
            if (!block.isOccupied && block.size >= requestSize) {
                block.size -= requestSize;
                if (block.size === 0) {
                    block.isOccupied = true;
                }
                console.log(`Allocated ${requestSize}KB.`);
                this.displayMemory();
                return;
            }
        }
        console.log(`Failed to allocate ${requestSize}KB. Not enough memory.`);
    }

    deallocate(originalSize, deallocateSize) {
        for (let block of this.memoryBlocks) {
            if (block.isOccupied && block.size === 0 && originalSize === deallocateSize) {
                block.size = originalSize;
                block.isOccupied = false;
                console.log(`Deallocated ${deallocateSize}KB.`);
                this.displayMemory();
                return;
            }
        }
        console.log(`Failed to deallocate ${deallocateSize}KB. Block not found.`);
    }

    displayMemory() {
        console.log("Memory Blocks:");
        for (let block of this.memoryBlocks) {
            console.log(`${block.size}KB ${block.isOccupied ? "(Occupied)" : "(Free)"}`);
        }
    }
}

// Simulate the dynamic memory allocation
const allocator = new MemoryAllocator();

// Display initial memory blocks
allocator.displayMemory();

// Simulate allocation requests
allocator.allocate(10);  // Try to allocate 10KB
allocator.allocate(5);   // Try to allocate 5KB

// Simulate deallocation requests
allocator.deallocate(10, 10);  // Try to deallocate 10KB
