---
layout: post
title: "Primer - Java common mistakes"
date: 2025-05-12
author: unattributed
categories: [java]
tags: [secure-coding, java, code-review]
---

# **Java Common Coding Mistakes - Cheat Sheet**  

### **1. NullPointerException (NPE)**  
- **Mistake:** Calling methods on `null` objects.  
- **Fix:**  
  ```java
  if (obj != null) {  
      obj.method();  
  }  
  // Or use Optional:  
  Optional.ofNullable(obj).ifPresent(o -> o.method());  
  ```

### **2. == vs. equals()**  
- **Mistake:** Using `==` for object comparison.  
- **Fix:**  
  ```java
  String s1 = "hello", s2 = new String("hello");  
  System.out.println(s1.equals(s2)); // true (content comparison)  
  ```

### **3. Immutable Strings**  
- **Mistake:** Concatenating in loops (creates many objects).  
- **Fix:** Use `StringBuilder`:  
  ```java
  StringBuilder sb = new StringBuilder();  
  for (int i = 0; i < 10; i++) sb.append(i);  
  String result = sb.toString();  
  ```

### **4. Forgetting `break` in Switch**  
- **Mistake:** Missing `break` causes fall-through.  
- **Fix:**  
  ```java
  switch (x) {  
      case 1: System.out.println("One"); break;  
      case 2: System.out.println("Two"); break;  
      default: System.out.println("Unknown");  
  }  
  ```

### **5. Resource Leaks**  
- **Mistake:** Not closing streams/files.  
- **Fix:** Use try-with-resources:  
  ```java
  try (FileInputStream fis = new FileInputStream("file.txt")) {  
      // Read file  
  } // Automatically closes  
  ```

### **6. Misusing `ArrayList` vs. `LinkedList`**  
- **Mistake:** Using `LinkedList` for frequent random access.  
- **Fix:**  
  - `ArrayList` → Fast access (`O(1)`).  
  - `LinkedList` → Fast insertions/deletions (`O(1)`).  

### **7. Ignoring `ConcurrentModificationException`**  
- **Mistake:** Modifying a collection while iterating.  
- **Fix:** Use `Iterator.remove()` or `CopyOnWriteArrayList`:  
  ```java
  Iterator<Integer> it = list.iterator();  
  while (it.hasNext()) {  
      if (it.next() == 2) it.remove(); // Safe removal  
  }  
  ```

### **8. Overriding `equals()` Without `hashCode()`**  
- **Mistake:** Breaking the `hashCode` contract.  
- **Fix:** Override both:  
  ```java
  @Override  
  public int hashCode() {  
      return Objects.hash(id, name);  
  }  
  ```

### **9. Using Raw Types**  
- **Mistake:** Not using generics.  
- **Fix:** Always specify type:  
  ```java
  List<String> list = new ArrayList<>(); // Not `List list`  
  ```

### **10. Integer Division**  
- **Mistake:** Forgetting floating-point division.  
- **Fix:** Cast to `double`:  
  ```java
  double result = (double) a / b;  
  ```

### **11. Static vs. Instance Methods/Variables**  
- **Mistake:** Accessing instance members from `static` methods.  
- **Fix:** Make variable `static` or use an instance.  

### **12. Unchecked Exceptions**  
- **Mistake:** Catching `Exception` instead of specific ones.  
- **Fix:** Catch precise exceptions:  
  ```java
  try { ... }  
  catch (IOException e) { ... } // Not just `Exception`  
  ```

### **13. Mutable `Date` Objects**  
- **Mistake:** Using outdated `java.util.Date`.  
- **Fix:** Use `java.time` (Java 8+):  
  ```java
  LocalDate date = LocalDate.now(); // Immutable  
  ```

### **14. Infinite Loops**  
- **Mistake:** Missing loop termination.  
- **Fix:** Ensure exit condition:  
  ```java
  while (true) {  
      if (condition) break;  
  }  
  ```

### **15. Incorrect `equals()` Implementation**  
- **Mistake:** Not handling `null` or wrong types.  
- **Fix:** Follow the contract:  
  ```java
  @Override  
  public boolean equals(Object o) {  
      if (this == o) return true;  
      if (o == null || getClass() != o.getClass()) return false;  
      MyClass obj = (MyClass) o;  
      return Objects.equals(field, obj.field);  
  }  
  ```

---

**Best Practices:**  
✔ Use `final` for constants.  
✔ Prefer `interface` types (e.g., `List<String> list = new ArrayList<>()`).  
✔ Avoid `float` for precise calculations (use `BigDecimal`).  
✔ Always override `toString()` for debugging.  

*Keep this sheet handy to avoid common pitfalls!*
[↑ Back to Top](#java-common-coding-mistakes---cheat-sheet)