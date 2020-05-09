# Which one to use, multi-processing or multi-threading?

- [Which one to use, multi-processing or multi-threading?](#which-one-to-use-multi-processing-or-multi-threading)
  - [Definition of Process](#definition-of-process)
  - [Definition of Thread](#definition-of-thread)
  - [How to choose](#how-to-choose)
  - [Warning](#warning)

## Definition of Process

From [Wiki](<https://en.wikipedia.org/wiki/Process_(computing)>)

> In computing, a **process** is an instance of a computer program that is being executed.
> It contains the program code and its current activity.
> Depending on the operating system (OS), a process may be made up of multiple threads of execution that execute instructions concurrently.

## Definition of Thread

From [Wiki](<https://en.wikipedia.org/wiki/Thread_(computing)>)

> In computer science, a **thread** of execution is the smallest sequence of programmed instructions that can be managed independently by a scheduler, which is typically a part of the operating system.
> The implementation of threads and processes differs between operating systems, but in most cases a thread is a component of a process.
> Multiple threads can exist within one process, executing concurrently and sharing resources such as memory, while different processes do not share these resources.
> In particular, the threads of a process share its executable code and the values of its variables at any given time.

## How to choose

Basic, a process can have multiple threads.
So, if the function is asking for multiple threads computing, one should use multi-processing method.
Otherwise, your multi-threading code will be running **extremely slow** since only one thread is executing.

## Warning

The use of multi-processing method is not all good.
The processes are separated from each other, so the computing should be of minimal interaction.

My suggestions is quite simple, which follows three steps:

1. Compute in a process.
2. Save results in the disk.
3. Collect them after all is done.
