---
layout: post
title: "Primer - C++ common mistakes"
date: 2025-05-12
author: unattributed
categories: [c++]
tags: [secure-coding, c++, code-review]
---

# **C++ Common Coding Mistakes Cheat Sheet**  

## **1. Memory Management**  
- **Memory Leaks**: Forgetting to `delete` dynamically allocated memory.  
  ```cpp
  int *p = new int[10]; // Must call delete[] p;
  ```  
- **Double Free**: Calling `delete` or `free()` on already freed memory.  
- **Dangling Pointers**: Using pointers after memory is freed.  
  ```cpp
  int *p = new int(5);
  delete p;
  *p = 10; // Undefined behavior!
  ```  
- **Smart Pointers**: Prefer `unique_ptr`, `shared_ptr` over raw pointers.  

## **2. Undefined Behavior**  
- **Uninitialized Variables**: Always initialize variables.  
  ```cpp
  int x; // Bad  
  int y = 0; // Good  
  ```  
- **Buffer Overflow**: Accessing beyond array bounds.  
  ```cpp
  int arr[5];
  arr[5] = 10; // Undefined behavior!
  ```  
- **Signed/Unsigned Mismatch**: Comparing signed and unsigned integers.  
  ```cpp
  for (int i = 0; i < v.size(); i++) // v.size() is size_t (unsigned)  
  ```  

## **3. Object Lifecycle & Copying**  
- **Shallow Copy**: Default copy constructor/assignment may cause double-free.  
  ```cpp
  class BadClass {  
    int *data;  
  public:  
    ~BadClass() { delete data; } // Need custom copy constructor & operator=  
  };  
  ```  
- **Rule of 5**: If you define one of (destructor, copy/move constructor, copy/move assignment), define all.  

## **4. STL Pitfalls**  
- **Iterator Invalidation**: Modifying containers while iterating.  
  ```cpp
  std::vector<int> v = {1, 2, 3};  
  for (auto it = v.begin(); it != v.end(); ++it) {  
    if (*it == 2) v.erase(it); // Invalidates iterator!  
  }  
  ```  
- **Reserve vs Resize**: `reserve()` only allocates, `resize()` also constructs.  

## **5. Common Syntax Errors**  
- **Missing `break` in `switch`**:  
  ```cpp
  switch (x) {  
    case 1: doSomething(); // Falls through!  
    case 2: break;  
  }  
  ```  
- **Misplaced Semicolons**:  
  ```cpp
  if (x > 0); { doSomething(); } // Always executes!  
  ```  

## **6. Thread Safety**  
- **Race Conditions**: Shared data accessed without locks.  
  ```cpp
  std::mutex mtx;  
  void unsafe() { counter++; }  
  void safe() { std::lock_guard<std::mutex> lock(mtx); counter++; }  
  ```  
- **Deadlocks**: Lock multiple mutexes in the same order.  

## **7. Compiler Warnings**  
- **Always enable warnings**:  
  ```sh
  g++ -Wall -Wextra -pedantic
  ```  
- **Fix `unused variable`, `implicit cast` warnings**.  

## **8. Performance Issues**  
- **Pass by Value**: Use `const &` for large objects.  
  ```cpp
  void slow(std::string s);  
  void fast(const std::string &s);  
  ```  
- **`std::endl` vs `\n`**: `std::endl` flushes buffer unnecessarily.  

## **9. Exceptions & Error Handling**  
- **Catching Exceptions by Value**:  
  ```cpp
  try { throw std::runtime_error("Error"); }  
  catch (std::exception &e) { /* Good */ }  
  catch (std::exception e) { /* Bad (slicing) */ }  
  ```  
- **RAII**: Use destructors for cleanup (e.g., files, locks).  

## **10. C++11+ Best Practices**  
- **Use `nullptr` instead of `NULL` or `0`**.  
- **Use `auto` to avoid type redundancy (but not everywhere!)**.  
- **`override` keyword for virtual functions**.  

---  
**Debug Tools**: Valgrind, AddressSanitizer (`-fsanitize=address`), `gdb`.  
**Static Analysis**: Clang-Tidy, Cppcheck.  

*Keep this handy to avoid common pitfalls!* 🚀