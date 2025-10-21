#!/usr/bin/env python3
"""
Comprehensive test for Henotace AI Python SDK v1.2.0
Tests both chat completion and classwork generation functionality
"""

import asyncio
import json
import time
from henotace_ai import HenotaceAI, create_tutor, SessionSubject, InMemoryConnector

async def test_chat_completion():
    """Test chat completion functionality"""
    print("💬 Testing Chat Completion Functionality")
    print("=" * 50)
    
    api_key = "henotace_dev_WiYGGqY1LnXWJiDGfDi0cXHk27mlOBII"
    sdk = HenotaceAI(api_key=api_key)
    
    test_cases = [
        {
            "name": "Basic Math Question",
            "history": [{'role': 'user', 'content': 'Hello, I need help with math'}],
            "input": "What is 2 + 2?",
            "subject": "mathematics",
            "topic": "basic arithmetic"
        },
        {
            "name": "Algebra Problem",
            "history": [
                {'role': 'user', 'content': 'I need help with algebra'},
                {'role': 'assistant', 'content': 'I\'d be happy to help you with algebra! What specific topic are you working on?'}
            ],
            "input": "How do I solve 2x + 5 = 13?",
            "subject": "mathematics",
            "topic": "algebra"
        },
        {
            "name": "Science Question",
            "history": [{'role': 'user', 'content': 'I\'m studying science'}],
            "input": "Explain photosynthesis briefly",
            "subject": "science",
            "topic": "biology"
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print(f"   Input: {test_case['input']}")
        
        try:
            start_time = time.time()
            response = sdk.complete_chat(
                history=test_case['history'],
                input_text=test_case['input'],
                subject=test_case['subject'],
                topic=test_case['topic']
            )
            end_time = time.time()
            
            ai_response = response.get('ai_response', '')
            response_time = end_time - start_time
            
            print(f"   ✅ Success: {len(ai_response)} characters")
            print(f"   ⏱️ Response time: {response_time:.2f} seconds")
            print(f"   📝 Response preview: {ai_response[:100]}...")
            
            results.append({
                "test": test_case['name'],
                "status": "SUCCESS",
                "response_length": len(ai_response),
                "response_time": response_time,
                "preview": ai_response[:100]
            })
            
        except Exception as e:
            print(f"   ❌ Failed: {str(e)}")
            results.append({
                "test": test_case['name'],
                "status": "FAILED",
                "error": str(e)
            })
    
    return results

async def test_classwork_generation():
    """Test classwork generation functionality"""
    print("\n📝 Testing Classwork Generation Functionality")
    print("=" * 50)
    
    api_key = "henotace_dev_WiYGGqY1LnXWJiDGfDi0cXHk27mlOBII"
    sdk = HenotaceAI(api_key=api_key)
    
    # Create detailed conversation history for classwork generation
    conversation_history = [
        {'role': 'user', 'content': 'I need help understanding linear equations'},
        {'role': 'assistant', 'content': 'Linear equations are equations where the highest power of the variable is 1. For example, 2x + 3 = 7 is a linear equation.'},
        {'role': 'user', 'content': 'How do I solve 2x + 5 = 13?'},
        {'role': 'assistant', 'content': 'To solve 2x + 5 = 13, you need to isolate x. First, subtract 5 from both sides: 2x = 8. Then divide both sides by 2: x = 4.'},
        {'role': 'user', 'content': 'What about equations with fractions like (1/2)x + 3 = 7?'},
        {'role': 'assistant', 'content': 'For equations with fractions, you can multiply both sides by the denominator to eliminate the fraction. For (1/2)x + 3 = 7, multiply by 2: x + 6 = 14, then solve: x = 8.'},
        {'role': 'user', 'content': 'How do I check if my answer is correct?'},
        {'role': 'assistant', 'content': 'To check your answer, substitute the value back into the original equation. For example, if x = 4, then 2(4) + 5 = 8 + 5 = 13, which matches the right side.'}
    ]
    
    test_cases = [
        {
            "name": "Easy Difficulty - 3 Questions",
            "question_count": 3,
            "difficulty": "easy",
            "subject": "mathematics",
            "topic": "linear equations"
        },
        {
            "name": "Medium Difficulty - 5 Questions", 
            "question_count": 5,
            "difficulty": "medium",
            "subject": "mathematics",
            "topic": "linear equations"
        },
        {
            "name": "Hard Difficulty - 4 Questions",
            "question_count": 4,
            "difficulty": "hard",
            "subject": "mathematics",
            "topic": "linear equations"
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print(f"   Subject: {test_case['subject']}")
        print(f"   Topic: {test_case['topic']}")
        print(f"   Questions: {test_case['question_count']}")
        print(f"   Difficulty: {test_case['difficulty']}")
        
        try:
            start_time = time.time()
            classwork = sdk.generate_classwork(
                history=conversation_history,
                subject=test_case['subject'],
                topic=test_case['topic'],
                question_count=test_case['question_count'],
                difficulty=test_case['difficulty']
            )
            end_time = time.time()
            
            questions = classwork.get('questions', [])
            response_time = end_time - start_time
            
            print(f"   ✅ Success: {len(questions)} questions generated")
            print(f"   ⏱️ Response time: {response_time:.2f} seconds")
            
            # Show first question as preview
            if questions:
                first_question = questions[0]
                question_text = first_question.get('question', 'No question text')
                print(f"   📋 Sample question: {question_text[:80]}...")
                
                # Show question type and options if available
                if first_question.get('type'):
                    print(f"   🎯 Question type: {first_question['type']}")
                if first_question.get('options'):
                    print(f"   📝 Options: {len(first_question['options'])} choices")
            
            results.append({
                "test": test_case['name'],
                "status": "SUCCESS",
                "questions_generated": len(questions),
                "response_time": response_time,
                "sample_question": questions[0].get('question', '') if questions else '',
                "question_type": questions[0].get('type', '') if questions else ''
            })
            
        except Exception as e:
            print(f"   ❌ Failed: {str(e)}")
            results.append({
                "test": test_case['name'],
                "status": "FAILED",
                "error": str(e)
            })
    
    return results

async def test_tutor_functionality():
    """Test tutor-based functionality"""
    print("\n👨‍🏫 Testing Tutor-Based Functionality")
    print("=" * 50)
    
    api_key = "henotace_dev_WiYGGqY1LnXWJiDGfDi0cXHk27mlOBII"
    sdk = HenotaceAI(api_key=api_key, storage=InMemoryConnector())
    
    try:
        # Create a tutor
        print("1. Creating Math Tutor...")
        tutor = await create_tutor(
            sdk=sdk,
            student_id="test_student_001",
            tutor_name="Math Tutor",
            subject=SessionSubject(
                id="mathematics",
                name="Mathematics", 
                topic="Algebra"
            )
        )
        print(f"   ✅ Tutor created: {tutor.tutor_id}")
        
        # Set up tutor persona
        print("\n2. Setting up tutor persona...")
        tutor.set_persona("You are an enthusiastic math tutor who loves to help students understand algebra. You explain concepts clearly and use step-by-step examples.")
        print("   ✅ Persona set successfully")
        
        # Simulate conversation
        print("\n3. Simulating tutoring conversation...")
        conversation_messages = [
            "I need help with solving equations",
            "Can you show me how to solve 3x - 7 = 14?",
            "What about checking my answer?",
            "How do I solve equations with variables on both sides?"
        ]
        
        for i, message in enumerate(conversation_messages, 1):
            print(f"   {i}. Student: {message}")
            try:
                response = await tutor.send(message)
                print(f"      Tutor: {response[:80]}...")
            except Exception as e:
                print(f"      ❌ Error: {e}")
                return {"status": "FAILED", "error": f"Tutor conversation failed: {e}"}
        
        # Generate classwork from conversation
        print("\n4. Generating classwork from conversation...")
        try:
            classwork = await tutor.generate_classwork(
                question_count=4,
                difficulty='medium'
            )
            
            questions = classwork.get('questions', [])
            print(f"   ✅ Generated {len(questions)} questions from conversation")
            
            if questions:
                print("   📋 Sample generated question:")
                print(f"      {questions[0].get('question', 'No question text')}")
            
            return {
                "status": "SUCCESS",
                "tutor_id": tutor.tutor_id,
                "conversation_messages": len(conversation_messages),
                "questions_generated": len(questions),
                "sample_question": questions[0].get('question', '') if questions else ''
            }
            
        except Exception as e:
            print(f"   ❌ Classwork generation failed: {e}")
            return {"status": "FAILED", "error": f"Classwork generation failed: {e}"}
            
    except Exception as e:
        print(f"❌ Tutor functionality failed: {e}")
        return {"status": "FAILED", "error": f"Tutor creation failed: {e}"}

async def test_error_handling():
    """Test error handling"""
    print("\n🛡️ Testing Error Handling")
    print("=" * 50)
    
    # Test with invalid API key
    print("1. Testing invalid API key...")
    try:
        invalid_sdk = HenotaceAI(api_key="invalid_key_test")
        invalid_sdk.complete_chat(
            history=[{'role': 'user', 'content': 'test'}],
            input_text="test message"
        )
        print("   ❌ Should have failed with invalid API key")
        return {"status": "FAILED", "error": "Invalid API key was not rejected"}
    except Exception as e:
        if "401" in str(e) or "Invalid API key" in str(e) or "API error" in str(e):
            print("   ✅ Invalid API key properly rejected")
        else:
            print(f"   ⚠️ Unexpected error: {e}")
    
    # Test with valid API key but invalid parameters
    print("\n2. Testing invalid parameters...")
    try:
        valid_sdk = HenotaceAI(api_key="henotace_dev_WiYGGqY1LnXWJiDGfDi0cXHk27mlOBII")
        # Test with empty history
        response = valid_sdk.complete_chat(
            history=[],
            input_text="test message"
        )
        print("   ✅ Empty history handled gracefully")
    except Exception as e:
        print(f"   ⚠️ Empty history error: {e}")
    
    return {"status": "SUCCESS"}

async def main():
    """Run all tests"""
    print("🚀 Henotace AI Python SDK v1.2.0 - Comprehensive Test Suite")
    print("=" * 70)
    print(f"API Key: henotace_dev_WiYGGqY1LnXWJiDGfDi0cXHk27mlOBII")
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    all_results = {
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
        "api_key": "henotace_dev_WiYGGqY1LnXWJiDGfDi0cXHk27mlOBII",
        "sdk_version": "1.2.0"
    }
    
    # Run all tests
    chat_results = await test_chat_completion()
    classwork_results = await test_classwork_generation()
    tutor_results = await test_tutor_functionality()
    error_results = await test_error_handling()
    
    all_results.update({
        "chat_completion": chat_results,
        "classwork_generation": classwork_results,
        "tutor_functionality": tutor_results,
        "error_handling": error_results
    })
    
    # Summary
    print("\n📊 Test Results Summary")
    print("=" * 70)
    
    chat_success = sum(1 for r in chat_results if r.get('status') == 'SUCCESS')
    classwork_success = sum(1 for r in classwork_results if r.get('status') == 'SUCCESS')
    
    print(f"💬 Chat Completion: {chat_success}/{len(chat_results)} tests passed")
    print(f"📝 Classwork Generation: {classwork_success}/{len(classwork_results)} tests passed")
    print(f"👨‍🏫 Tutor Functionality: {'✅ PASSED' if tutor_results.get('status') == 'SUCCESS' else '❌ FAILED'}")
    print(f"🛡️ Error Handling: {'✅ PASSED' if error_results.get('status') == 'SUCCESS' else '❌ FAILED'}")
    
    total_tests = len(chat_results) + len(classwork_results) + 2  # +2 for tutor and error handling
    total_passed = chat_success + classwork_success + (1 if tutor_results.get('status') == 'SUCCESS' else 0) + (1 if error_results.get('status') == 'SUCCESS' else 0)
    
    print(f"\n🎯 Overall: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        print("🎉 ALL TESTS PASSED! Python SDK v1.2.0 is working perfectly!")
    else:
        print("⚠️ Some tests failed. Check the detailed results above.")
    
    # Save results to file
    with open('test_results.json', 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n💾 Detailed results saved to: test_results.json")
    
    return all_results

if __name__ == "__main__":
    asyncio.run(main())
