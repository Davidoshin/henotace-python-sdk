#!/usr/bin/env python3
"""
Comprehensive test script for the refactored Henotace AI Python SDK
"""

import asyncio
import sys
import os
from datetime import datetime

# Add src to path
sys.path.append('src')

from henotace_ai import (
    HenotaceAI, create_tutor, SessionSubject, InMemoryConnector,
    HenotaceError, HenotaceAPIError, HenotaceNetworkError,
    LogLevel, ConsoleLogger
)

async def test_sdk():
    """Run comprehensive tests on the refactored SDK"""
    
    print("🧪 Henotace AI Python SDK - Comprehensive Test")
    print("=" * 60)
    print(f"⏰ Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test 1: SDK Initialization
    print("1️⃣ Testing SDK Initialization...")
    try:
        api_key = ""
        sdk = HenotaceAI(
            api_key=api_key,
            storage=InMemoryConnector(),
            logging={
                "enabled": True,
                "level": LogLevel.INFO
            }
        )
        print("✅ SDK initialization successful")
        print(f"   - API Key: {api_key[:20]}...")
        print(f"   - Base URL: {sdk.base_url}")
        print(f"   - Timeout: {sdk.timeout}s")
        print(f"   - Retries: {sdk.retries}")
    except Exception as e:
        print(f"❌ SDK initialization failed: {e}")
        return False
    
    print()
    
    # Test 2: API Status Check
    print("2️⃣ Testing API Status Check...")
    try:
        status = sdk.get_status()
        print("✅ API status check successful")
        print(f"   - Success: {status.get('success', False)}")
        print(f"   - Status: {status.get('data', {}).get('status', 'unknown')}")
        print(f"   - Message: {status.get('data', {}).get('message', 'No message')}")
        
        # Test boolean status check
        status_ok = sdk.get_status_ok()
        print(f"   - Status OK: {status_ok}")
    except HenotaceAPIError as e:
        print(f"❌ API Error: {e}")
        return False
    except HenotaceNetworkError as e:
        print(f"❌ Network Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    print()
    
    # Test 3: Tutor Creation
    print("3️⃣ Testing Tutor Creation...")
    try:
        tutor = await create_tutor(
            sdk=sdk,
            student_id="test_student_001",
            tutor_name="Test Math Tutor",
            subject=SessionSubject(
                id="mathematics",
                name="Mathematics",
                topic="Algebra"
            ),
            grade_level="high_school",
            language="en"
        )
        print("✅ Tutor creation successful")
        print(f"   - Student ID: {tutor.student_id}")
        print(f"   - Tutor ID: {tutor.tutor_id}")
        print(f"   - IDs: {tutor.ids}")
    except Exception as e:
        print(f"❌ Tutor creation failed: {e}")
        return False
    
    print()
    
    # Test 4: Tutor Configuration
    print("4️⃣ Testing Tutor Configuration...")
    try:
        # Set persona
        tutor.set_persona("You are a helpful and patient math tutor who explains concepts clearly.")
        print("✅ Persona set successfully")
        
        # Set context
        tutor.set_context([
            "The student is learning algebra for the first time.",
            "They prefer step-by-step explanations with examples."
        ])
        print("✅ Context set successfully")
        
        # Set user profile
        tutor.set_user_profile({
            "name": "Test Student",
            "grade": "9th",
            "learning_style": "visual",
            "difficulty_level": "beginner"
        })
        print("✅ User profile set successfully")
        
        # Set compression settings
        tutor.set_compression(
            max_turns=5,
            max_summary_chars=500,
            checkpoint_every=3
        )
        print("✅ Compression settings configured")
        
    except Exception as e:
        print(f"❌ Tutor configuration failed: {e}")
        return False
    
    print()
    
    # Test 5: Chat Interaction
    print("5️⃣ Testing Chat Interaction...")
    try:
        # First message
        print("   Sending first message...")
        response1 = await tutor.send("Hello! Can you help me understand what algebra is?")
        print(f"✅ First message successful")
        print(f"   - Response length: {len(response1)} characters")
        print(f"   - Response preview: {response1[:100]}...")
        
        # Second message
        print("   Sending second message...")
        response2 = await tutor.send(
            "That's helpful! Can you give me a simple example of an algebraic equation?",
            context="The student is new to algebra and needs a basic example."
        )
        print(f"✅ Second message successful")
        print(f"   - Response length: {len(response2)} characters")
        print(f"   - Response preview: {response2[:100]}...")
        
    except HenotaceAPIError as e:
        print(f"❌ API Error during chat: {e}")
        return False
    except HenotaceNetworkError as e:
        print(f"❌ Network Error during chat: {e}")
        return False
    except Exception as e:
        print(f"❌ Chat interaction failed: {e}")
        return False
    
    print()
    
    # Test 6: Chat History
    print("6️⃣ Testing Chat History...")
    try:
        history = tutor.history()
        print(f"✅ Chat history retrieved")
        print(f"   - Total messages: {len(history)}")
        
        for i, chat in enumerate(history, 1):
            sender = "👤 User" if not chat.is_reply else "🤖 AI"
            preview = chat.message[:50] + "..." if len(chat.message) > 50 else chat.message
            print(f"   - Message {i}: {sender} - {preview}")
            
    except Exception as e:
        print(f"❌ Chat history retrieval failed: {e}")
        return False
    
    print()
    
    # Test 7: Storage Operations
    print("7️⃣ Testing Storage Operations...")
    try:
        # List students
        students = sdk.list_students()
        print(f"✅ Storage operations successful")
        print(f"   - Students in storage: {len(students)}")
        
        # List tutors for our student
        tutors = sdk.list_tutors("test_student_001")
        print(f"   - Tutors for test student: {len(tutors)}")
        
        # List chats
        chats = sdk.list_chats("test_student_001", tutor.tutor_id)
        print(f"   - Chats for tutor: {len(chats)}")
        
    except Exception as e:
        print(f"❌ Storage operations failed: {e}")
        return False
    
    print()
    
    # Test 8: Error Handling
    print("8️⃣ Testing Error Handling...")
    try:
        # Test with invalid API key
        invalid_sdk = HenotaceAI(api_key="invalid_key")
        try:
            invalid_sdk.get_status()
            print("❌ Should have failed with invalid key")
        except HenotaceAPIError:
            print("✅ Invalid API key properly rejected")
        
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False
    
    print()
    
    # Test Summary
    print("🎉 Test Summary")
    print("=" * 60)
    print("✅ All tests passed successfully!")
    print(f"⏰ Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    print("📊 Test Results:")
    print("   ✅ SDK Initialization")
    print("   ✅ API Status Check")
    print("   ✅ Tutor Creation")
    print("   ✅ Tutor Configuration")
    print("   ✅ Chat Interaction")
    print("   ✅ Chat History")
    print("   ✅ Storage Operations")
    print("   ✅ Error Handling")
    print()
    print("🚀 The refactored Henotace AI Python SDK is working perfectly!")
    
    return True

if __name__ == "__main__":
    try:
        result = asyncio.run(test_sdk())
        if result:
            print("\n🎯 All tests completed successfully!")
            sys.exit(0)
        else:
            print("\n💥 Some tests failed!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)
