(function() {
  window.addEventListener("load", function() {
    var $ = django.jQuery;

    var _initializedCache = [];

    function initJSONForm(index, element) {
      // Check if element has already been initialized
      if (_initializedCache.indexOf(element) !== -1) {
        return;
      }

      var dataInput = element;
      var dataInputId = element.id;

      var config = JSON.parse(element.dataset.djangoJsonform);
      config.dataInputId =
        config.data = JSON.parse(config.data);

      var containerId = element.id + '_jsonform';

      var container = $(element).prev("[data-django-jsonform-container]");
      container.attr('id', element.id + '_jsonform');

      config.containerId = containerId;
      config.dataInputId = dataInputId;

      var jsonForm = reactJsonForm.createForm(config);
      if (config.validateOnSubmit) {
        var form = dataInput.form;
        form.addEventListener("submit", function(e) {
          var errorlist = container.parentElement.previousElementSibling;
          var hasError;

          if (errorlist && errorlist.classList.contains("errorlist"))
            hasError = true;
          else
            hasError = false;

          var validation = jsonForm.validate();

          if (!validation.isValid) {
            e.preventDefault();

            if (!hasError) {
              errorlist = document.createElement("ul");
              errorlist.setAttribute("class", "errorlist");
              var errorli = document.createElement("li");
              errorli.textContent = "Please correct the errors below.";
              errorlist.appendChild(errorli);

              container.parentElement.parentElement.insertBefore(
                errorlist, container.parentElement
              );
            }

            errorlist.scrollIntoView();
          } else {
            if (hasError)
              errorlist.remove();
          }
          jsonForm.update({ errorMap: validation.errorMap });
        });
      }
      jsonForm.render();
      _initializedCache.push(element);
    }

    // This logic taken from django-autocomplete-light:
    // https://github.com/yourlabs/django-autocomplete-light/blob/master/src/dal/static/autocomplete_light/autocomplete_light.js#L120
    $.fn.excludeTemplateForms = function() {
      // exclude elements that contain '__prefix__' in their id
      // these are used by django formsets for template forms
      return this.not("[id*=__prefix__]").filter(function() {
        // exclude elements that contain '-empty-' in their ids
        // these are used by django-nested-admin for nested template formsets
        // note that the filter also ensures that 'empty' is not actually the related_name for some relation
        // by ensuring that it is not surrounded by numbers on both sides
        return !this.id.match(/-empty-/) || this.id.match(/-\d+-empty-\d+-/);
      });
    };

    /**
     * Helper function to determine if the element is being dragged, so that we
     * don't initialize the json form fields. They will get initialized when the dragging stops.
     *
     * @param element The element to check
     * @returns {boolean}
     */
    function isDraggingElement(element) {
      return "classList" in element && element.classList.contains("ui-sortable-helper");
    }

    function initializeAllForNode(parentElement) {
      $(parentElement).find("[data-django-jsonform]").excludeTemplateForms().each(initJSONForm)
    }

    // Initialize all json form fields already on the page.
    initializeAllForNode(document);

    // Setup listeners to initialize all json form fields as they get added to the page.
    if ("MutationObserver" in window) {
      new MutationObserver(function(mutations) {
        var mutationRecord;
        var addedNode;

        for (var i = 0; i < mutations.length; i++) {
          mutationRecord = mutations[i];

          if (mutationRecord.addedNodes.length > 0) {
            for (var j = 0; j < mutationRecord.addedNodes.length; j++) {
              addedNode = mutationRecord.addedNodes[j];
              if (isDraggingElement(addedNode)) return;
              initializeAllForNode(addedNode);
            }
          }
        }
      }).observe(document.documentElement, { childList: true, subtree: true });
    } else {
      $(document).on("DOMNodeInserted", function(e) {
        if (isDraggingElement(e.target)) return;
        initializeAllForNode(e.target);
      });
    }
  });

})();