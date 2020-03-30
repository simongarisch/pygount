"""
Tests to summarize analyses of multiple source codes.
"""
from pygount.analysis import SourceAnalysis, SourceState
from pygount.summary import LanguageSummary, ProjectSummary


def test_can_repr_language_summary():
    language_summary = LanguageSummary("Python")
    language_summary.add(SourceAnalysis("some.py", "Python", "some", 2, 3, 4, 5, SourceState.analyzed))
    expected_language_summary_repr = (
        "LanguageSummary(language='Python', file_count=1, code=2, documentation=3, empty=4, string=5)"
    )
    assert repr(language_summary) == expected_language_summary_repr
    assert repr(language_summary) == str(language_summary)


def test_can_repr_pseudo_language_summary():
    language_summary = LanguageSummary("__empty__")
    language_summary.add(SourceAnalysis("some.py", "__empty__", "some", 0, 0, 0, 0, SourceState.empty))
    expected_language_summary_repr = "LanguageSummary(language='__empty__', file_count=1)"
    assert repr(language_summary) == expected_language_summary_repr
    assert repr(language_summary) == str(language_summary)


def test_can_summarize_project_with_multiple_files_of_same_language():
    source_analyses = (
        SourceAnalysis("some.py", "Python", "some", 300, 70, 4, 2, SourceState.analyzed),
        SourceAnalysis("other.py", "Python", "some", 700, 30, 6, 3, SourceState.analyzed),
    )

    project_summary = ProjectSummary()
    for source_analysis in source_analyses:
        project_summary.add(source_analysis)

    assert set(project_summary.language_to_language_summary_map.keys()) == {"Python"}
    assert project_summary.total_file_count == 2
    assert project_summary.total_code_count == 1000
    assert project_summary.total_documentation_count == 100
    assert project_summary.total_empty_count == 10
    assert project_summary.total_string_count == 5


def test_can_summarize_project_with_multiple_files_of_different_languages():
    source_analyses = (
        SourceAnalysis("some.py", "Python", "some", 1000, 100, 10, 3, SourceState.analyzed),
        SourceAnalysis("some.sh", "Bash", "some", 200, 20, 5, 2, SourceState.analyzed),
    )

    project_summary = ProjectSummary()
    for source_analysis in source_analyses:
        project_summary.add(source_analysis)

    assert set(project_summary.language_to_language_summary_map.keys()) == {"Bash", "Python"}
    assert project_summary.total_file_count == 2
    assert project_summary.total_code_count == 1200
    assert project_summary.total_documentation_count == 120
    assert project_summary.total_empty_count == 15
    assert project_summary.total_string_count == 5


def test_can_summarize_project_with_pseudo_languages():
    source_analyses = (
        SourceAnalysis("empty.py", "__empty__", "some", 0, 0, 0, 0, SourceState.empty),
        SourceAnalysis("generated.py", "__generated__", "some", 1, 2, 3, 4, SourceState.generated),
        SourceAnalysis("binary .bin", "__binary__", "some", 0, 0, 0, 0, SourceState.binary),
    )
    expected_languages = {source_analysis.language for source_analysis in source_analyses}

    project_summary = ProjectSummary()
    for source_analysis in source_analyses:
        project_summary.add(source_analysis)

    assert project_summary.total_file_count == 3
    assert set(project_summary.language_to_language_summary_map.keys()) == expected_languages
    assert project_summary.total_code_count == 0
    assert project_summary.total_documentation_count == 0
    assert project_summary.total_empty_count == 0
    assert project_summary.total_string_count == 0


def test_can_repr_empty_project_summary():
    project_summary = ProjectSummary()
    assert repr(project_summary) == "ProjectSummary(total_file_count=0, total_line_count=0, languages=[]"
    assert repr(project_summary) == str(project_summary)
