===
mixed-poor-examples: collection, python, educational
===
AI-focused windings that produce Python code for science fairs. Accessible from elementary to high school.


--
my_first_ai: python, classifier, simple
--
Teach AI to recognize my drawings.

@task: classify
Draw 3 things you like. AI will learn to tell them apart.

@drawings: cat, sun, house
@interface: webcam, draw_on_screen
@feedback: happy_sounds, confusion_meter
@explain: which_parts_helped_decide

--
emotion_detector: python, science_fair, face_recognition
--
Can AI understand how my friends feel?

@hypothesis: AI can detect basic emotions from faces
@emotions: happy, sad, surprised, neutral
@visualization: emoji_overlay, confidence_bars
@data: collect_from_family, permission_first
@fairness: works_for_everyone

--
pet_translator: python, audio, ml
--
What is my pet trying to say?

@animals: dog, cat, hamster, bird
@sounds: bark, meow, squeak, chirp
@patterns: hungry, playful, warning, happy
@output: speech_bubble, confidence_score
@science: correlation_not_causation

--
plant_health_ai: python, image_classification, helper
--
AI plant doctor for my garden.

@camera: phone, raspberry_pi
@conditions: healthy, needs_water, too_much_sun, bugs
@alerts: gentle_notifications
@learning: improves_with_feedback
@science_process: hypothesis, data, results

--
homework_helper: python, nlp, study_buddy
--
AI that explains things like a friend would.

@subjects: math, science, history
@style: patient, encouraging, visual
@features: step_by_step, draw_diagrams, check_understanding
@ethics: helps_learn, not_just_answers

--
recyclable_sorter: python, computer_vision, environmental
--
AI to help sort recycling correctly.

@categories: plastic, paper, glass, compost, trash
@camera: webcam, live_feedback
@education: why_each_matters
@gamification: points, earth_helper_badges
@data: local_recycling_rules

--
music_mood_generator: python, generative_ai, creative
--
AI that makes music based on colors.

@input: color_picker, drawing_pad
@mapping: warm_colors→happy, cool_colors→calm
@output: simple_melodies, instrument_choices
@science: synesthesia_exploration
@share: export_as_ringtone

--
story_continue_ai: python, text_generation, creative_writing
--
AI that helps finish your stories.

@start_with: "Once upon a time..."
@choices: suggest_three_paths
@illustration: generate_scene_images
@safety: age_appropriate, positive_themes
@learn: story_structure, creativity

--
movement_coach: python, pose_detection, health
--
AI that helps me exercise better.

@exercises: jumping_jacks, stretches, dance_moves
@feedback: real_time, encouraging
@tracking: progress_calendar, streak_counter
@fun: unlock_new_moves, celebration_animations
@privacy: all_processing_local

--
food_freshness_checker: python, image_analysis, practical
--
Is this still good to eat?

@items: fruits, vegetables, leftovers
@indicators: color_changes, texture, mold_detection
@output: safe, questionable, definitely_not
@education: why_food_spoils, reducing_waste
@parent_mode: send_grocery_suggestions

--
friend_finder: python, interests_matching, social
--
AI that suggests who might be good friends.

@interests: books, games, sports, music, coding
@matching: similar_AND_complementary
@privacy: no_personal_data_stored
@suggestions: conversation_starters
@science: network_theory_basics

--
dream_visualizer: python, text_to_image, creative
--
Draw what I dreamed about last night.

@input: voice_description, keywords
@style: dreamy, watercolor, surreal
@elements: combine_unexpected_things
@journal: save_dream_diary
@science: how_memory_works

===
implementation_notes: guide
===
Each winding should produce Python code that:
1. Uses pre-trained models when possible (HuggingFace, TensorFlow.js)
2. Runs on modest hardware (M2 MacBook perfect)
3. Has visual, interactive output
4. Includes "How AI Works" explanations
5. Collects data ethically
6. Produces science fair ready visualizations

@python_libraries:
- transformers  # HuggingFace models
- opencv-python  # Computer vision
- sounddevice  # Audio input
- streamlit  # Quick UIs
- matplotlib  # Graphs for science fair
- PIL  # Image processing

@teaching_moments:
Every project should naturally introduce:
- What is training data?
- How does AI learn patterns?
- Why does accuracy matter?
- What are ethics in AI?
- How to present findings?

@progression:
Age 6-8: Recognition tasks (my_first_ai, pet_translator)
Age 9-11: Analysis tasks (emotion_detector, recyclable_sorter)
Age 12-14: Generation tasks (music_mood_generator, story_continue_ai)
Age 15+: Research tasks (custom models, paper writing)