# Proposed next build — normal coal supply to 9 electric-fed iron furnaces
Not built yet. Validate against fresh state. Copper/iron science feeds are now automatic; furnace fuel remains manual.

Source: personal coal chest(-17.5,-55.5), powered electric drill(-17.5,-57.5) outputs0.5coal/s, enough9furnaces0.2025coal/s. Export inserter(-16.5,-55.5)dir12 toUGBELT INPUT(-15.5,-55.5)floweast4, OUTPUT(-10.5,-55.5)buildparameterWEST12 (gameautooutputactual4). CrossesCuMAINx-13.5 underground. Newpole(-14.5,-53.5)connects existing(-20.5,-54.5), powersoutputinserter. Check existingpole20.5,54.5 negative coords in state.

FromUGoutput(-10.5,-55.5) needsflowturnnorth: outputflow4 goesE, so addnormal(-9.5,-55.5)dir0; thenMAINcoalcolumnx-9.5 northy-56.5..-123.5, turneast atlast. MAINeastrowy-123.5 x-8.5..58.5dir4. (Earlierthoughtx-10.5columnwrongbecauseUGexitfloweastneedsadjacentturn!) Watchtree/rockcollision; mine normally orroute. x-9.5 crossesoldironpowerliney-96.5 betweenpoles-13.5/-6.5, nointerference. x-9.5 crossesnoCuMAINatx-13.5. Eastrowy-123.5 northofdrills118.5;existingnewpole(-20.5,-124.5)notinrow.

Threebranchpickup insertersatx50.5,54.5,58.5 y-122.5dir0 takecoalfrommainnorthy-123.5 andputUGinputy-121.5. EachbranchSOUTHflow8:
- UGinput(x,-121.5)dir8 →UGoutput(x,-116.5)buildparameter0 => actualoutput8.
- Normalbelt(x,-115.5),(x,-114.5)dir8.
- UGinput(x,-113.5)dir8 →UGoutput(x,-108.5)buildparameter0.
- Normalbelt(x,-107.5),(x,-106.5)dir8.
- UGinput(x,-105.5)dir8 →UGoutput(x,-100.5)buildparameter0.
Allpairsdistance5 validatedprimaryprototypeyellowmax_distance5. Theycrossdrillrowsandironcollectionbelts112.5/104.5underground; endpointtilesavoidcollectionnormalbelts49.5/53.5/57.5aty113.5/105.5.

Ninefuelinsertersatx49.5,53.5,57.5 y-116.5,-108.5,-100.5dir4 pickEcoalfromx50.5/54.5/58.5, putW intofurnace48/52/56(theseare2x2centersat48/52/56,y-116/-108/-100). Existingpowercovers8, last(49.5,-100.5)needsnewpole(49.5,-101.5)connectedexisting(46.5,-99.5); checkplacementnexttoe.drill47.5,-102.5. Threebranchpickupy-122.5 needpoles near y-121.5! Existingironpoles49.5,-115.5 dist7 supplynotcover. Addpole(49.5,-121.5), (53.5,-121.5), (57.5,-121.5) BUTsameyUGinputatx50.5/54.5/58.5 adjacent okay; existingdrill55.5,-118.5 top120 so121.5outside. New49.5,-121.5wireexisting49.5,-115.5 distance6;53.5wireexisting53.5,-115.5 distance6;57.5wireexisting57.5,-114.5 distance7. Coversbranchpickupx+1,y-122.5.

Materialrough:~138mainnormalbelts+12branchnormal=150;10UGpairs20items (baghas4UGitemsfrom10crafted-6usedCu);12inserters(3pickup+9fuel)+1sourceexport=13;5poles(1source+3pickup+1lastfuel). Craft~90beltrecipes(180items)and8UGrecipes(16items,consumes40beltitems+80Fe), accountingbagremaining~24normalbelts. Totalrequired161? Generateactualcounts programmatically thenensure>=neededplusreserve. LastbagFe~800likelyenough, verify. Newcoalbuswilldrawpersonalcoalchest; don'tremoveallfuturecoalforhandrefill. Furnacefuelinventorylimits50meansincomingbacksupafter50each;coalflowwillselfregulate.

Afterautomationverify9fuelinserters actualworking/fullfuel,coalUGlinkedSOUTH,ironcollectionbeltsstillFeonly. Old4ironfurnaces/3burnerdrillsremainmanual;9automatedfurnaces169Fe/minenoughcurrentgreen82.5Fe/min+futureadditional. Copperfuel7furnacesstillmanual40eachrefilled802680, good~30min. RedscienceFe/Custillmanualbutbuffers. Plasticscoalinput200refilled~800000,goodseveralminutes. Sulfurresearch~30%wasstarvedCu; nowbothgreenworkingandshouldadvance.
