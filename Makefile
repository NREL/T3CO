generate_pydocs: 
	pipx install pydoc-markdown
	pydoc-markdown -I . -p t3co --render-toc > docs/functions/CodeReference.md
	pydoc-markdown -I . -m t3co/sweep --render-toc > docs/functions/sweep.md
	pydoc-markdown -I . -m t3co/run/run_scenario --render-toc > docs/functions/run_scenario.md
	pydoc-markdown -I . -m t3co/run/generateinputs --render-toc > docs/functions/generateinputs.md
	pydoc-markdown -I . -m t3co/run/Global --render-toc > docs/functions/Global.md
	pydoc-markdown -I . -m t3co/tco/tcocalc --render-toc > docs/functions/tcocalc.md
	pydoc-markdown -I . -m t3co/tco/tco_analysis --render-toc > docs/functions/tco_analysis.md
	pydoc-markdown -I . -m t3co/tco/opportunity_cost --render-toc > docs/functions/opportunity_cost.md
	pydoc-markdown -I . -m t3co/tco/tco_stock_emissions --render-toc > docs/functions/tco_stock_emissions.md
	pydoc-markdown -I . -m t3co/objectives/accel --render-toc > docs/functions/accel.md
	pydoc-markdown -I . -m t3co/objectives/fueleconomy --render-toc > docs/functions/fueleconomy.md
	pydoc-markdown -I . -m t3co/objectives/gradeability --render-toc > docs/functions/gradeability.md
	pydoc-markdown -I . -m t3co/moopack/moo --render-toc > docs/functions/moo.md
	
