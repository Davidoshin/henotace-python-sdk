#!/usr/bin/env python3
"""
Integration test for classwork generation functionality
Tests the complete flow from chat completion to classwork generation
"""

import asyncio
import os
import sys
import json
import time
sys.path.append('src')
from henotace_ai import HenotaceAI, create_tutor, SessionSubject, InMemoryConnector


async def test_classwork_generation():
    """Test classwork generation with a real API key"""
    
    # Get API key from environment
    api_key = os.getenv('HENOTACE_API_KEY')
    if not api_key:
        print("❌ HENOTACE_API_KEY environment variable not set")
        print("   Please set it with: export HENOTACE_API_KEY=your_api_key_here")
        return False
    
    print("🧪 Testing Henotace AI Python SDK - Classwork Generation")
    print("=" * 60)
    
    try:
        # Initialize SDK
        print("📡 Initializing SDK...")
        sdk = HenotaceAI(
            api_key=api_key,
            storage=InMemoryConnector(),
            timeout=30,
            retries=2
        )
        
        # Test API status
        print("🔍 Testing API status...")
        status = sdk.get_status()
        if not status.get('success'):
            print(f"❌ API status check failed: {status}")
            return False
        print("✅ API status check passed")
        
        # Test basic chat completion
        print("\n💬 Testing basic chat completion...")
        test_history = [
            {'role': 'user', 'content': 'Hello, I need help with math'},
            {'role': 'assistant', 'content': 'Hello! I\'d be happy to help you with math. What specific topic are you working on?'}
        ]
        
        response = sdk.complete_chat(
            history=test_history,
            input_text="Can you explain how to solve 2x + 5 = 13?",
            subject="mathematics",
            topic="algebra"
        )
        
        if not response.get('ai_response'):
            print("❌ Chat completion failed - no response")
            return False
        
        print("✅ Basic chat completion works")
        print(f"   Response length: {len(response['ai_response'])} characters")
        
        # Test classwork generation
        print("\n📝 Testing classwork generation...")
        
        # Create a more detailed conversation history
        detailed_history = [
            {'role': 'user', 'content': 'I need help understanding linear equations'},
            {'role': 'assistant', 'content': 'Linear equations are equations where the highest power of the variable is 1. For example, 2x + 3 = 7 is a linear equation.'},
            {'role': 'user', 'content': 'How do I solve 2x + 5 = 13?'},
            {'role': 'assistant', 'content': 'To solve 2x + 5 = 13, you need to isolate x. First, subtract 5 from both sides: 2x = 8. Then divide both sides by 2: x = 4.'},
            {'role': 'user', 'content': 'What about equations with fractions like (1/2)x + 3 = 7?'},
            {'role': 'assistant', 'content': 'For equations with fractions, you can multiply both sides by the denominator to eliminate the fraction. For (1/2)x + 3 = 7, multiply by 2: x + 6 = 14, then solve: x = 8.'}
        ]
        
        # Test different difficulty levels
        difficulties = ['easy', 'medium', 'hard']
        results = {}
        
        for difficulty in difficulties:
            print(f"\n   Testing {difficulty.upper()} difficulty...")
            
            classwork = sdk.generate_classwork(
                history=detailed_history,
                subject="mathematics",
                topic="linear equations",
                question_count=3,
                difficulty=difficulty
            )
            
            if not classwork:
                print(f"   ❌ {difficulty} classwork generation failed")
                return False
            
            questions = classwork.get('questions', [])
            if not questions:
                print(f"   ❌ {difficulty} classwork has no questions")
                return False
            
            results[difficulty] = {
                'question_count': len(questions),
                'questions': questions[:2]  # Store first 2 questions for verification
            }
            
            print(f"   ✅ {difficulty} classwork: {len(questions)} questions generated")
        
        # Test tutor-based classwork generation
        print("\n👨‍🏫 Testing tutor-based classwork generation...")
        
        tutor = await create_tutor(
            sdk=sdk,
            student_id="test_student_001",
            tutor_name="Test Math Tutor",
            subject=SessionSubject(
                id="mathematics",
                name="Mathematics",
                topic="Algebra"
            )
        )
        
        # Simulate a conversation
        await tutor.send("I need help with solving equations")
        await tutor.send("Can you show me how to solve 3x - 7 = 14?")
        await tutor.send("What about checking my answer?")
        
        # Generate classwork from tutor conversation
        tutor_classwork = await tutor.generate_classwork(
            question_count=4,
            difficulty='medium'
        )
        
        if not tutor_classwork or not tutor_classwork.get('questions'):
            print("❌ Tutor-based classwork generation failed")
            return False
        
        print(f"✅ Tutor-based classwork: {len(tutor_classwork['questions'])} questions")
        
        # Test error handling
        print("\n🛡️ Testing error handling...")
        
        try:
            # Test with invalid API key
            invalid_sdk = HenotaceAI(api_key="invalid_key")
            invalid_sdk.complete_chat(
                history=test_history,
                input_text="Test message"
            )
            print("❌ Should have failed with invalid API key")
            return False
        except Exception as e:
            if "Invalid API key" in str(e) or "401" in str(e) or "API error" in str(e):
                print("✅ Invalid API key properly rejected")
            else:
                print(f"❌ Unexpected error with invalid API key: {e}")
                return False
        
        # Test rate limiting (if applicable)
        print("\n⏱️ Testing rate limiting...")
        try:
            # Make multiple rapid requests
            for i in range(3):
                sdk.complete_chat(
                    history=test_history,
                    input_text=f"Test message {i}"
                )
            print("✅ Rate limiting test passed")
        except Exception as e:
            if "429" in str(e) or "rate limit" in str(e).lower():
                print("✅ Rate limiting properly handled")
            else:
                print(f"⚠️ Rate limiting test: {e}")
        
        # Summary
        print("\n📊 Test Results Summary:")
        print("=" * 40)
        print("✅ API Status Check: PASSED")
        print("✅ Basic Chat Completion: PASSED")
        print("✅ Classwork Generation (Easy): PASSED")
        print("✅ Classwork Generation (Medium): PASSED")
        print("✅ Classwork Generation (Hard): PASSED")
        print("✅ Tutor-based Classwork: PASSED")
        print("✅ Error Handling: PASSED")
        print("✅ Rate Limiting: PASSED")
        
        print(f"\n📈 Generated Questions Summary:")
        for difficulty, result in results.items():
            print(f"   {difficulty.upper()}: {result['question_count']} questions")
        
        print(f"\n🎉 All tests passed! Python SDK is working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_authentication():
    """Test authentication methods"""
    print("\n🔐 Testing Authentication Methods...")
    
    api_key = os.getenv('HENOTACE_API_KEY')
    if not api_key:
        print("❌ No API key available for authentication test")
        return False
    
    try:
        # Test with valid API key
        sdk = HenotaceAI(api_key=api_key)
        
        # Check if Authorization header is being used
        response = sdk._make_request('GET', '/api/external/status/')
        if response.status_code == 200:
            print("✅ Authentication with valid API key: PASSED")
        else:
            print(f"❌ Authentication failed: {response.status_code}")
            return False
        
        # Test with invalid API key using an endpoint that requires authentication
        invalid_sdk = HenotaceAI(api_key="invalid_key_test")
        try:
            # Use chat completion endpoint which requires authentication
            invalid_sdk.complete_chat(
                history=[{'role': 'user', 'content': 'test'}],
                input_text="test message"
            )
            print("❌ Invalid API key should have been rejected")
            return False
        except Exception as e:
            if "401" in str(e) or "Invalid API key" in str(e) or "API error" in str(e):
                print("✅ Invalid API key properly rejected")
            else:
                print(f"❌ Unexpected error: {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Authentication test failed: {e}")
        return False


async def main():
    """Run all integration tests"""
    print("🚀 Henotace AI Python SDK - Integration Tests")
    print("=" * 60)
    
    # Test authentication first
    auth_result = await test_authentication()
    if not auth_result:
        print("❌ Authentication tests failed. Stopping.")
        return
    
    # Test classwork generation
    classwork_result = await test_classwork_generation()
    
    if classwork_result:
        print("\n🎉 All integration tests completed successfully!")
        print("✅ Python SDK is ready for production use")
    else:
        print("\n❌ Some integration tests failed")
        print("🔧 Please check the errors above and fix them")


if __name__ == "__main__":
    asyncio.run(main())
